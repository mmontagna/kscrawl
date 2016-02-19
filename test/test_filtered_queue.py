import unittest, time
from crawl.queues.Local import LocalQueue
from crawl.queues.Filter import FilterQueue

class TestFilteredQueue(unittest.TestCase):

  def test_filter(self):
      Q  = FilterQueue(LocalQueue(), lambda x: 'a.com' in x)

      links = ['a.com', 'a.com/test', 'c.com']
      Q.send(links)
      self.assertEquals(['a.com', 'a.com/test'], sorted([x for x in Q]))

  def test_filter_all(self):
      Q  = FilterQueue(LocalQueue(), lambda x: False)

      links = ['a.com', 'a.com/test', 'c.com']
      Q.send(links)
      self.assertEquals([], [x for x in Q])

  def test_filter_none(self):
      Q  = FilterQueue(LocalQueue(), lambda x: True)

      links = ['a.com', 'a.com/test', 'c.com']
      Q.send(links)
      self.assertEquals(links, sorted([x for x in Q]))

if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestFilteredQueue)
  unittest.TextTestRunner(verbosity=2).run(suite)