import redis, os

class RedisSet:

  def __init__(self, name_space='default'):
    self.redis = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)
    self.redis_key = name_space + ':set'
  def add(self, x):
    self.redis.sadd(self.redis_key, hash(x))

  def __contains__(self, x):
    #Hash(x) makes this inaccurate but prevents giant URLS from causing problems.
    return self.redis.sismember(self.redis_key, hash(x))
