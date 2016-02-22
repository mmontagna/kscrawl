from crawl.processors.Abstract import AbstractProcessor
from collections import defaultdict
import uuid, cStringIO, gzip, json, boto3, os, datetime
from urlparse import urlparse

class S3Store(AbstractProcessor):
  def __init__(self, bucket, buffer_size=100):
    self.output = defaultdict(lambda: defaultdict(lambda : {}))
    self.aux_out = defaultdict(lambda: defaultdict(lambda : {}))
    self.bucket = bucket
    self.s3 = None
    self.buffer_size = buffer_size

  def process(self, url, response):
    domain = urlparse(url).netloc
    cleaned = unicode(response.raw, errors='replace')
    self.output[domain][response.request.crawl_id][url] = {'content' : cleaned, 'accessed' : response.accessed}
    self.aux_out[domain][response.request.crawl_id][url] = {'feature_hash' : response.feature_vector, 'accessed' : response.accessed}
    self.checkBuffer()

  """ Check all buffers and flush if full. """
  def checkBuffer(self):
    for group in self.output:
      for crawl_id in self.output[group]:
        if (len(self.output[group][crawl_id].keys()) > self.buffer_size):
          self.write(group, crawl_id)

  def write(self, group, crawl_id):
    self.writeToS3(group, 'content', 'object', crawl_id, json.dumps(self.output[group][crawl_id]))
    self.writeToS3(group, 'auxiliary', 'index', crawl_id, json.dumps(self.aux_out[group][crawl_id]))
    self.aux_out[group][crawl_id] = {}

  def writeToS3(self, group, folder, name, crawl_id, content):
    if (not self.s3):
      self.s3 = boto3.resource('s3')

    object_id = str(uuid.uuid4())
    key = os.path.join(group, crawl_id, folder, object_id + '.' + name + '.json.gz')

    fgz = cStringIO.StringIO()
    with gzip.GzipFile(mode='wb', fileobj=fgz) as gzip_obj:
        gzip_obj.write(content)

    print "Writing", name, object_id, group, "for crawl", crawl_id

    self.s3.Bucket(self.bucket).Object(key).put(Body=fgz.getvalue())

  def close(self):
    for group in self.output:
      for crawl_id in self.output[group]:
          self.write(group, crawl_id)
