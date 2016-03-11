from crawl.processors.Abstract import AbstractProcessor
from collections import defaultdict
import uuid, cStringIO, gzip, json, boto3, os, datetime
from time import time
from urlparse import urlparse

class S3Store(AbstractProcessor):
  def __init__(self, buffer_size=1000, periodic_flush=5):
    #domain.crawl_id.folder.name
    self.raw_output = defaultdict(lambda: defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : []))))
    self.output = defaultdict(lambda: defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : []))))
    self.last_processed_times = defaultdict(lambda: defaultdict(lambda : time()))
    self.crawl_folders = {}
    self.flush_time = periodic_flush
    self.max_buffer_size = buffer_size

    self.buckets = {}
    self.crawl_buckets = {}

  def get_bucket_for(self, bucket):
    if bucket not in self.buckets:
      self.buckets[bucket] = boto3.resource('s3').Bucket(bucket)
    return self.buckets[bucket]


  def tick(self):
    for domain, crawl_id in self.domains_and_crawls():
      if (self.buffer_expired(domain, crawl_id)):
        self.write(domain, crawl_id)

  def process(self, crawlRequest, response):
    url = crawlRequest.link
    domain = urlparse(url).netloc
    for output in response.output:
      if (output.raw):
        self.raw_output[domain][response.request.crawl_id][output.folder][output.name] = output.content
      else:
        self.crawl_folders[response.request.crawl_id] = response.request.output_prefix
        self.crawl_buckets[response.request.crawl_id] = response.request.output_bucket

        self.output[domain][response.request.crawl_id][output.folder][output.name].append((url, (output.content, response.accessed)))
        self.last_processed_times[domain][response.request.crawl_id] = time()
    self.checkBuffer()

  def buffer_size(self, domain, crawl_id):
    source = self.output[domain][crawl_id]
    return max([len(source[key][key2]) for key, key2 in [(key, key2) for key in source for key2 in source[key]]])

  def domains_and_crawls(self):
    return [(domain, crawl_id) for domain in self.output for crawl_id in self.output[domain]]

  def buffer_expired(self, domain, crawl_id):
    if (time() - self.last_processed_times[domain][crawl_id] > self.flush_time):
      return True
    return False

  """ Check all buffers and flush if full. """
  def checkBuffer(self):
    for domain, crawl_id in self.domains_and_crawls():
      if (self.buffer_size(domain, crawl_id) > self.max_buffer_size or self.buffer_expired(domain, crawl_id)):
        self.write(domain, crawl_id)

  def write(self, group, crawl_id):
    object_ids = defaultdict(lambda : str(uuid.uuid4()))
    try:
      for folder, name in [(folder, name) for folder in self.raw_output[group][crawl_id] for name in self.raw_output[group][crawl_id][folder]]:
        try:
          crawl_folder = self.crawl_folders[crawl_id]
          content = self.raw_output[group][crawl_id][folder][name]
          self.rawWriteToS3(crawl_folder, group, folder, name, crawl_id, content, object_ids[group + crawl_id])
          self.raw_output[group][crawl_id][folder][name] = []
        except Exception as e:
          print e
    finally:
      del self.raw_output[group][crawl_id]

    try:
      for folder, name in [(folder, name) for folder in self.output[group][crawl_id] for name in self.output[group][crawl_id][folder]]:
        try:
          print 'writing', group, crawl_id, folder, name
          content = json.dumps(dict([(x[0], x[1]) for x in self.output[group][crawl_id][folder][name]]))
          crawl_folder = self.crawl_folders[crawl_id]
          self.writeToS3(crawl_folder, group, folder, name, crawl_id, content, object_ids[group + crawl_id])
          self.output[group][crawl_id][folder][name] = []
        except Exception as e:
          print e
    finally:
      del self.output[group][crawl_id]

  def rawWriteToS3(self, crawl_folder, group, folder, name, crawl_id, content, object_id):
    key = os.path.join(crawl_folder, crawl_id, group, folder, object_id + name)
    try:
      self.get_bucket_for(self.crawl_buckets[crawl_id]).Object(key).put(Body=content)
    except Exception as e:
      print e
  def writeToS3(self, crawl_folder, group, folder, name, crawl_id, content, object_id):
    key = os.path.join(crawl_folder, crawl_id, group, folder, name + '.' + object_id + '.json.gz')
    fgz = cStringIO.StringIO()
    with gzip.GzipFile(mode='wb', fileobj=fgz) as gzip_obj:
        gzip_obj.write(content)
    self.get_bucket_for(self.crawl_buckets[crawl_id]).Object(key).put(Body=fgz.getvalue())

  def close(self):
    for group, crawl_id in self.domains_and_crawls():
          self.write(group, crawl_id)
