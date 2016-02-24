import argparse
from crawl.queues.Redis import RedisQueue
import pprint, json

parser = argparse.ArgumentParser(description='Add URLs to start a crawl')
parser.add_argument('--name_space', default='default', help='The crawl namespace.')
args = parser.parse_args()

RQ = RedisQueue(name_space=args.name_space)
pp = pprint.PrettyPrinter(indent=2)

print RQ.number_clients(), 'workers'
print RQ.items_in_queues(),
#print pp.pprint(RQ.queue_states())

print json.dumps(RQ.queue_states(), indent=2, separators=(',', ': '))