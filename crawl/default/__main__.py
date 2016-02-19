
import inspect, uuid
from crawl.crawler import SimpleCrawler
from crawl.queues.Redis import RedisQueue
from crawl.sets import SimpleSet
from crawl.LinkCrawlRequest import LinkCrawlRequest
from crawl.http.Simple import SimpleHttp
from crawl.queues.Filter import FilterQueue
from crawl.processors.LocalFiles import LocalFileStore

def domain_hash(linkCrawlReq):
  from urlparse import urlparse
  import time
  dest = 0
  try:
    minute = int(time.time()) % (60*10)
    dest = hash(urlparse(linkCrawlReq.link).netloc + minute + linkCrawlReq.attempts)
  except:
    pass
  return dest

def domain_filter(domains):
  from urlparse import urlparse
  domains = domains
  def helper(linkCrawlReq):
    try:
      if urlparse(linkCrawlReq.link).netloc in domains:
        return True
    except:
      pass
    return False
  return helper


RQ = RedisQueue(name_space='crawltest', hash_function=domain_hash)
Q = FilterQueue(RQ, domain_filter(['marcomontagna.com', 'github.com']))

S = SimpleSet()
RQ.redis.flushdb()

Q.send([LinkCrawlRequest('http://marcomontagna.com', str(uuid.uuid4()))])
crawler = SimpleCrawler(Q, S, SimpleHttp(), LocalFileStore('./output'))

crawler.crawl()

#TO DO
"""
  CREATE processor which stores to S3
  Buffer records, grouped by domain, then write to s3
    (as a single gzip archive => better compression)

  key like: bucket/prefix + hash(domain) + crawl(id) + hash(content)
    content like: [raw response, url, time retrieved]

  Provide mechanism for iterating over reponses
    (will need to account for the gzip archive format).

  process(response, queue, set)


"""

print "HELLO"


# r.set('worker_x', 1)
# r.set('worker_y', 1)


#print len(r.keys('worker_*'))

#print [x for x, y in inspect.getmembers(r)]