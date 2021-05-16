import importlib, inspect, uuid, argparse, sys, os
from crawl.crawler import SimpleCrawler
from crawl.queues.Redis import RedisQueue
from crawl.sets import RedisSet
from crawl.LinkCrawlRequest import LinkCrawlRequest
from crawl.http.Simple import SimpleHttp
from crawl.processors.Abstract import AbstractProcessor


import crawl.default

try:
  parser = argparse.ArgumentParser(description='Run a default crawler')
  parser.add_argument('--name_space', default='default', help='The crawl namespace.')
  parser.add_argument('--global_throttle', default=None, help='Max req to make per second from this crawler', type=float)
  parser.add_argument('--processors', default=[], help='', nargs='+', type=str)
  args = parser.parse_args()

  Q = RedisQueue(name_space=args.name_space, hash_function=crawl.default.domain_hash)
  Q.allow_registration = True

  S = RedisSet()
  crawler = SimpleCrawler(Q, S, SimpleHttp())

  if (args.global_throttle):
    crawler.throttle_control = (1 / args.global_throttle)

  for processor in args.processors:
    processor =  importlib.import_module(processor)
    for name, obj in processor.__dict__.items():
      if inspect.isclass(obj) and issubclass(obj, AbstractProcessor) and obj is not AbstractProcessor:
        crawler.add_response_processor(obj())

  crawler.crawl()
except KeyboardInterrupt:
    print 'Interrupted'
    crawler.close()
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
