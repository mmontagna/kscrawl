import unittest, time
from crawl.queues.Local import LocalQueue

class TestLocalQueue(unittest.TestCase):

  def test_send_get(self):
      Q  = LocalQueue()
      links = ['a', 'b', 'c']
      Q.send(links)
      self.assertEquals(links, sorted([x for x in Q]))
if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestLocalQueue)
  unittest.TextTestRunner(verbosity=2).run(suite)