import uuid, argparse
from crawl.queues.Redis import RedisQueue
from crawl.LinkCrawlRequest import LinkCrawlRequest, domain_filter
import crawl.default



parser = argparse.ArgumentParser(description='Add URLs to start a crawl')
parser.add_argument('--name_space', default='default', help='The crawl namespace.')
parser.add_argument('--urls', help='URLs to start crawl with', nargs='*')
parser.add_argument('--depth', default=float('+inf'), help='Depth limit', type=int)
parser.add_argument('--restrict-to-origin', default=False, help='If true then dont crawl other domains')
args = parser.parse_args()

crawl_id = str(uuid.uuid4())

RQ = RedisQueue(name_space=args.name_space, hash_function=crawl.default.domain_hash)

if (args.restrict_to_origin):
  accept = domain_filter
else:
  accept = None

print "Adding", args.urls, 'to crawl', crawl_id, 'depth limit', args.depth
RQ.send([LinkCrawlRequest(url,
                          crawl_id=crawl_id,
                          depth_limit=args.depth,
                          accept=accept) for url in args.urls])
