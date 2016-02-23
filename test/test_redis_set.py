import unittest
from crawl.sets import RedisSet

class TestRedisSet(unittest.TestCase):

  def test_emptyset_contains_nothing(self):
    rs = RedisSet()
    rs.redis.flushdb()
    self.assertFalse('x' in rs)
    self.assertFalse('y' in rs)
    self.assertFalse('z' in rs)

  def test_add_contains(self):
    rs = RedisSet()
    rs.redis.flushdb()
    rs.add('x')
    rs.add('y')
    rs.add('z')
    self.assertTrue('x' in rs)
    self.assertTrue('y' in rs)
    self.assertTrue('z' in rs)

if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestRedisSet)
  unittest.TextTestRunner(verbosity=2).run(suite)
