import inspect, uuid, argparse, sys, os
from crawl.crawler import SimpleCrawler
from crawl.queues.Redis import RedisQueue
from crawl.sets import RedisSet
from crawl.LinkCrawlRequest import LinkCrawlRequest
from crawl.http.Simple import SimpleHttp
from crawl.processors.S3 import S3Store
from crawl.processors.PageVectorizer import PageVectorizer
import crawl.default

try:
  parser = argparse.ArgumentParser(description='Run a default crawler')
  parser.add_argument('--name_space', default='default', help='The crawl namespace.')
  parser.add_argument('--global_throttle', default=None, help='Max req to make per second from this crawler', type=float)
  args = parser.parse_args()

  Q = RedisQueue(name_space=args.name_space, hash_function=crawl.default.domain_hash)
  Q.allow_registration = True

  S = RedisSet()
  crawler = SimpleCrawler(Q, S, SimpleHttp())

  if (args.global_throttle):
    crawler.throttle_control = (1 / args.global_throttle)

  crawler.add_response_processor(PageVectorizer())
  crawler.add_response_processor(S3Store())

  crawler.crawl()
except KeyboardInterrupt:
    print 'Interrupted'
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)