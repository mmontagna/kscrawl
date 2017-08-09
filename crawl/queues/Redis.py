import redis, os, uuid
import dill as pickle
import random

from crawl.queues.Abstract import AbstractQueue

class RedisQueue(AbstractQueue):
  worker_marker_prefix = 'redisqueue:worker:marker:'

  def __init__(self, registration_expiration_ms=60000*5, hash_function=hash, name_space='default', allow_registration=False):
    self.allow_registration = allow_registration
    self.queue = []
    self.redis = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)
    self.uuid = str(uuid.uuid4())
    self.registration_expiration_ms = registration_expiration_ms
    self.name_space = name_space

    self.register()
    self.hash = hash_function

    self.last_num_clients = None
    self.queue = 'redisqueue:worker:queue:'

  def generate_worker_marker(self):
    return self.worker_marker_prefix + self.name_space + self.uuid

  def register(self):
    if (self.allow_registration):
      self.redis.psetex(self.generate_worker_marker(), self.registration_expiration_ms, 1)
      self.get_clients()

  def _destination_hash(self, thing):
    return self.hash(thing) % self.number_clients()

  def send(self, things):
    try:
      self.register()
      for thing in things:
        pickledObj = pickle.dumps(thing)
        self.redis.lpush(self.queue, pickledObj)
    except Exception as e:
      print "Send error"
      raise e

  def get(self):
    self.register()
    pickledObj = self.redis.rpop(self.queue)
    if (pickledObj is None):
      return None

    try:
      return pickle.loads(pickledObj)
    except Exception as e:
      print "RedisQueue: Unable to unpickle object req", e


  def all_items(self, limit=int(10e6)):
    pickles = self.redis.lrange(self.queue, 0, limit)
    cucumbers = [pickle.loads(pickledThing) for pickledThing in pickles]
    return cucumbers

  def items_in_queues(self):
    return self.redis.llen(self.queue)

  def get_clients(self):
    return self.redis.keys(self.worker_marker_prefix + self.name_space + '*')

  def _number_clients(self):
    return len(self.get_clients())

  def number_clients(self):
    return self._number_clients()

  def get_my_client_number(self):
    return sorted(self.get_clients()).index(self.generate_worker_marker())
