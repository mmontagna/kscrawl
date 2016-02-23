import unittest, time
from crawl.queues.Local import LocalQueue
from crawl.http.Response import Response
from crawl.LinkCrawlRequest import LinkCrawlRequest
from crawl.processors.PageVectorizer import PageVectorizer

class TestPageVectorizer(unittest.TestCase):
  pv = PageVectorizer()
  def test_send_get(self):

    request = LinkCrawlRequest('http://example.com/')
    response = Response('<html><body><h1>Crawling is fun<h1><p>Definitely!</body></html>', request)
    self.pv.process('http://example.com/', response)

    self.assertEquals('auxiliary', response.output[1].folder)
    self.assertEquals('feature_hash', response.output[1].name)
    self.assertIsNotNone(response.output[0].content)


  def test_text_split_correctly(self):
    resp = Response("<p>a test</p><p>Yep</p>", None)
    self.assertEquals(['a', 'test', 'yep'], self.pv.clean_and_filter(resp))

  def test_text_cleaned_correct(self):
    resp = Response("<p>This is, a Test.</p>", None)
    self.assertEquals(['this', 'is', 'a', 'test'], self.pv.clean_and_filter(resp))

  def test_hash_stability(self):
    '''
        Hardcode some expected word hash values, that way if something
        changes this test will fail and prompt investigation.
    '''
    resp = Response("<p>This is, a Test.</p>", None)
    words = "world the interesting sky ocean moon simple sets of things".split()
    expected = [(5, 1), (15, 1), (56, 1), (58, 1), (60, 1), (71, 1), (86, 1), (96, 1)]
    self.assertEquals(expected, self.pv.feature_vector(words))


if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestPageVectorizer)
  unittest.TextTestRunner(verbosity=2).run(suite)