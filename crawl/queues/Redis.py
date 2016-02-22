import redis, os, uuid
import cPickle as pickle
from crawl.queues.Abstract import AbstractQueue

class RedisQueue(AbstractQueue):
  queue_prefix = 'redisqueue:worker:queue:'
  worker_marker_prefix = 'redisqueue:worker:marker:'

  def __init__(self, registration_expiration_ms=60000, hash_function=hash, name_space='default'):
    self.queue = []
    self.redis = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)
    self.uuid = str(uuid.uuid4())
    self.registration_expiration_ms = registration_expiration_ms
    self.name_space = name_space

    self.register()
    self.hash = hash_function

    self.last_num_clients = None

  def generate_queue(self, worker_number):
    return self.queue_prefix + self.name_space + str(worker_number)

  def generate_worker_marker(self):
    return self.worker_marker_prefix + self.name_space + self.uuid

  def register(self):
    self.redis.psetex(self.generate_worker_marker(), self.registration_expiration_ms, 1)
    self.get_clients()

  def _destination_hash(self, thing):
    return self.hash(thing) % self.number_clients()

  def send(self, things):
    self.register()
    for thing in things:
      pickledObj = pickle.dumps(thing)
      self.redis.lpush(self.generate_queue(self._destination_hash(thing)), pickledObj)

  def get(self):
    pickledObj = self.redis.rpop(self.generate_queue(self.get_my_client_number()))
    thing = None
    try:
      thing  = pickle.loads(pickledObj)
    except:
      if thing is not None:
        print "RedisQueue: Unable to unpickle object req", pickledObj
      pass
    return thing

  def get_clients(self):
    return self.redis.keys(self.worker_marker_prefix + self.name_space + '*')

  def number_clients(self):
    next = len(self.get_clients())
    if (next < self.last_num_clients):
      delta = self.last_num_clients - next
      for i in range(self.last_num_clients, self.last_num_clients - delta, -1):
        self.rebalance(i - 1)

    self.last_num_clients = next
    return self.last_num_clients

  def rebalance(self, worker_number):
    v = self.redis.lpop(self.generate_queue(worker_number))
    i = 0
    while v is not None:
      i += 1
      self.redis.lpush(self.generate_queue(worker_number - 1), v)
      v = self.redis.lpop(self.generate_queue(worker_number))

  def get_my_client_number(self):
    return sorted(self.get_clients()).index(self.generate_worker_marker())
