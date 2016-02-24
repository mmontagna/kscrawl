import argparse, json
from crawl.queues.Redis import RedisQueue
from collections import defaultdict
from urlparse import urlparse

def summarize_state(RD):
  requests = RD.all_items()
  state = defaultdict(lambda: {'in_flight' : 0, 'domains' : defaultdict(lambda: 0)})
  for crawlRequest in requests:
    state[crawlRequest.crawl_id]['in_flight'] += 1
    state[crawlRequest.crawl_id]['domains'][urlparse(crawlRequest.link).netloc[:50]] +=1

  for key in state.keys():
    state[key]['domains'] = dict(state[key]['domains'])
  return {'num_workers': RQ.number_clients(), 'in_flight': RQ.items_in_queues(), 'crawls' : dict(state)}

parser = argparse.ArgumentParser(description='Add URLs to start a crawl')
parser.add_argument('--name_space', default='default', help='The crawl namespace.')
args = parser.parse_args()

RQ = RedisQueue(name_space=args.name_space)

print json.dumps(summarize_state(RQ), indent=2, separators=(',', ': '))