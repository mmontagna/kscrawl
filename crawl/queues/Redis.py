import redis, os, uuid
import dill as pickle
from crawl.queues.Abstract import AbstractQueue

class RedisQueue(AbstractQueue):


  def __init__(self, registration_expiration_ms=60000, hash_function=hash, name_space='default', allow_registration=False):
    self.allow_registration = allow_registration
    self.queue = []
    self.redis = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)
    self.uuid = str(uuid.uuid4())
    self.registration_expiration_ms = registration_expiration_ms
    self.name_space = name_space

    self.hash = hash_function

    self.last_num_clients = None
    self.queue_prefix = 'redisqueue:worker:queue:'
    self.worker_marker_prefix = 'redisqueue:worker:marker:'

  def send(self, things):
    for thing in things:
      pickledObj = pickle.dumps(thing)
      self.redis.lpush(self.queue_prefix, pickledObj)

  def get(self):
    pickledObj = self.redis.rpop(self.queue_prefix)
    if (pickledObj is None):
      return None

    try:
      return pickle.loads(pickledObj)
    except Exception as e:
      print "RedisQueue: Unable to unpickle object req", e


  def all_items(self, limit=int(10e6)):
    cucumbers = [pickle.loads(pickledThing) for pickledThing in self.redis.lrange(self.queue_prefix, 0, limit)]
    return cucumbers

  def items_in_queues(self):
    return self.redis.llen(self.queue_prefix)

  def number_clients(self):
    return -1
