from __future__ import print_function
import unittest
from crawl.queues import LocalQueue
from crawl.sets import SimpleSet
from crawl.crawler import SimpleCrawler
from crawl.http.Abstract import AbstractHttp
from crawl.http.Response import Response
from crawl.LinkCrawlRequest import LinkCrawlRequest, domain_filter
from mock import MagicMock
import mock
from attrdict import AttrDict

class FakeHttp(AbstractHttp):
  def __init__(self, responses):
    self.responses = responses

  def get(self, req):
    if (len(self.responses) > 0):
      temp = self.responses[0]
      self.responses = self.responses[1:]
    else:
      temp = ""
    return Response(temp, req)

class TestCrawler(unittest.TestCase):
  def make_processor_mock(self):
    return AttrDict({'process' : MagicMock(), 'tick' : MagicMock(), 'close': MagicMock()})
  def test_basic_crawl(self):
    Q = LocalQueue()

    S = SimpleSet()
    Q.send([LinkCrawlRequest('https://test.com')])
    mockHttp = FakeHttp(['<a href="https://test.com/1">l</a><a href="2">l</a><a href="/3">l</a>'] * 10)
    crawler = SimpleCrawler(Q, S, mockHttp)
    crawler.stop_on_empty()
    fakeProcessor = self.make_processor_mock()
    crawler.add_response_processor(fakeProcessor)
    crawler.crawl()
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://test.com/'), mock.ANY)
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://test.com/1'), mock.ANY)
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://test.com/2'), mock.ANY)
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://test.com/3'), mock.ANY)

  def test_stop_at_depth(self):
    Q = LocalQueue()

    S = SimpleSet()
    Q.send([LinkCrawlRequest('https://test.com')])
    responses = ['<a href="' + str(i) + '">l</a>' for i in range(0, 10)]
    mockHttp = FakeHttp(responses)
    crawler = SimpleCrawler(Q, S, mockHttp)
    crawler.depth_limit = 5
    crawler.stop_on_empty()
    fakeProcessor = self.make_processor_mock()
    crawler.add_response_processor(fakeProcessor)

    #Should consume 5 responses before hitting depth limit
    crawler.crawl()
    self.assertEqual(5, len(mockHttp.responses)) # Should be 5 responses left

  def test_stop_at_crawl_specific_depth_limits(self):
    Q = LocalQueue()
    S = SimpleSet()
    Q.send([LinkCrawlRequest('https://test.com', depth_limit=3)])
    responses = ['<a href="' + str(i) + '">l</a>' for i in range(0, 10)]
    mockHttp = FakeHttp(responses)
    crawler = SimpleCrawler(Q, S, mockHttp)
    crawler.stop_on_empty()
    fakeProcessor = self.make_processor_mock()
    crawler.add_response_processor(fakeProcessor)

    #Should consume 3 responses before hitting depth limit
    crawler.crawl()
    self.assertEqual(7, len(mockHttp.responses)) # Should be 5 responses left

  def setup_crawl_specific_filter(self, accept):
    Q = LocalQueue()
    S = SimpleSet()
    Q.send([LinkCrawlRequest('https://test.com', accept=accept)])
    responses = ['<a href="/' + str(i) + '">l</a><a href="https://nottest.com/' + str(i) + '">l</a>' for i in range(0, 2)]
    mockHttp = FakeHttp(responses)
    crawler = SimpleCrawler(Q, S, mockHttp)
    crawler.stop_on_empty()
    fakeProcessor = self.make_processor_mock()
    crawler.add_response_processor(fakeProcessor)

    crawler.crawl()
    return fakeProcessor

  def test_crawl_specific_filter(self):
    #Test filter does filter
    fakeProcessor = self.setup_crawl_specific_filter(domain_filter)
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://test.com/'), mock.ANY)
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://test.com/0'), mock.ANY)
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://test.com/1'), mock.ANY)
    self.assertEqual(3, len(fakeProcessor.process.call_args_list)) #No other calls => didn't crawl notest.com

    #Make sure we get the other urls without the filter
    fakeProcessor = self.setup_crawl_specific_filter(None)
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://nottest.com/0'), mock.ANY)
    fakeProcessor.process.assert_any_call(LinkCrawlRequest('https://nottest.com/1'), mock.ANY)



if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestCrawler)
  unittest.TextTestRunner(verbosity=2).run(suite)