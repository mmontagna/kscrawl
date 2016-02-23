from crawl.processors.Abstract import AbstractProcessor
from collections import defaultdict
import uuid, cStringIO, gzip, json, boto3, os, datetime
from urlparse import urlparse

class S3Store(AbstractProcessor):
  def __init__(self, bucket, buffer_size=100, s3_bucket_object=None):
    #domain.crawl_id.folder.name
    self.output = defaultdict(lambda: defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : []))))
    self.max_buffer_size = buffer_size

    self.bucket = bucket
    if (s3_bucket_object is not None):
      self.s3_bucket_object = s3_bucket_object
    else:
      self.s3_bucket_object = boto3.resource('s3').Bucket(self.bucket)

  def process(self, url, response):
    domain = urlparse(url).netloc
    for output in response.output:
      self.output[domain][response.request.crawl_id][output.folder][output.name].append((url, (output.content, response.accessed)))

    self.checkBuffer()

  def buffer_size(self, domain, crawl_id):
    source = self.output[domain][crawl_id]
    return max([len(source[key][key2]) for key, key2 in [(key, key2) for key in source for key2 in source[key]]])

  """ Check all buffers and flush if full. """
  def checkBuffer(self):
    for domain, crawl_id in [(domain, crawl_id) for domain in self.output for crawl_id in self.output[domain]]:
      if (self.buffer_size(domain, crawl_id) > self.max_buffer_size):
        self.write(domain, crawl_id)

  def write(self, group, crawl_id):
    for folder, name in [(folder, name) for folder in self.output[group][crawl_id] for name in self.output[group][crawl_id][folder]]:
      print 'writing', group, crawl_id, folder, name
      content = json.dumps(dict([(x[0], x[1]) for x in self.output[group][crawl_id][folder][name]]))
      self.writeToS3(group, folder, name, crawl_id, content)
    self.output[group][crawl_id][folder][name] = []

  def writeToS3(self, group, folder, name, crawl_id, content):
    object_id = str(uuid.uuid4())
    key = os.path.join('crawl', group, crawl_id, folder, name + '.' + object_id + '.json.gz')
    fgz = cStringIO.StringIO()
    with gzip.GzipFile(mode='wb', fileobj=fgz) as gzip_obj:
        gzip_obj.write(content)
    self.s3_bucket_object.Object(key).put(Body=fgz.getvalue())

  def close(self):
    for group in self.output:
      for crawl_id in self.output[group]:
          self.write(group, crawl_id)
