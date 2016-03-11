from crawl.processors.Abstract import AbstractProcessor
from collections import defaultdict
import os, gzip, json
from urlparse import urlparse

class LocalFileStore(AbstractProcessor):
  def __init__(self, folder):
    self.folder = folder
    try:
      os.mkdir(folder)
    except:
      pass
    self.output = defaultdict(lambda: defaultdict(lambda : []))

  def process(self, crawlRequest, response):
    url = crawlRequest.link
    domain = urlparse(url).netloc
    self.output[domain][response.request.crawl_id].append((url, response.raw))

  def close(self):
    for domain in self.output:
      for crawl_id in self.output[domain]:
        with gzip.open(os.path.join(self.folder, domain + '_' + crawl_id + '.json.gz'), 'w') as f:
          f.write(json.dumps(self.output[domain][crawl_id]))
