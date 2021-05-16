import uuid, argparse, datetime
from crawl.queues.Redis import RedisQueue
from crawl.LinkCrawlRequest import LinkCrawlRequest, domain_filter, create_domains_filter
import crawl.default



parser = argparse.ArgumentParser(description='Add URLs to start a crawl')
parser.add_argument('--name_space', default='default', help='The crawl namespace.')
parser.add_argument('--urls', required=True, help='URLs to start crawl with', nargs='*')
parser.add_argument('--depth', default=float('+inf'), help='Depth limit', type=int)
parser.add_argument('--output_bucket', default=None)
parser.add_argument('--screenshot', default=False, help='whether to take screen shots. (requires a selenium server)')
parser.add_argument('--output_prefix', default='crawl', help='enclosing s3 prefix')
parser.add_argument('--restrict-origin', action='store_true', default=False, help='If true then dont crawl other domains')
parser.add_argument('--restrict-domains', nargs='*', default=False, help='If true then only follow links on given domains.')

args = parser.parse_args()

crawl_id = str(datetime.date.today()) + '-' + str(uuid.uuid4())

RQ = RedisQueue(name_space=args.name_space, hash_function=crawl.default.domain_hash)

if (args.restrict_origin):
  print "setting origin filter"
  accept = domain_filter
elif (args.restrict_domains):
  accept = create_domains_filter(args.restrict_domains)
else:
  accept = None

if (args.urls[0].startswith('file://')):
  args.urls = open(args.urls[0][len('file://'):]).read().split()

print "Adding", len(args.urls), 'to crawl', crawl_id, 'depth limit', args.depth
RQ.send([LinkCrawlRequest(url,
                          crawl_id=crawl_id,
                          depth_limit=args.depth,
                          accept=accept,
                          output_prefix=args.output_prefix,
                          bucket=args.output_bucket,
                          options = {'screenshot' : args.screenshot}
                          ) for url in args.urls])
