import argparse
from crawl.queues.Redis import RedisQueue

parser = argparse.ArgumentParser(description="Reset a crawler's state")
parser.add_argument('--name_space', default='default', help='The crawl namespace.')
args = parser.parse_args()

RQ = RedisQueue(name_space=args.name_space)
RQ.redis.flushdb()