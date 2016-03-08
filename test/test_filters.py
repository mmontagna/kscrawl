import unittest, boto3, time
from crawl.processors import S3Store
from crawl.http.Response import Response
from crawl.LinkCrawlRequest import LinkCrawlRequest, domain_filter, create_domains_filter

class TestFilters(unittest.TestCase):

  def test_domain_filter(self):
    r = Response('', LinkCrawlRequest('http://example.com/'))
    self.assertTrue(domain_filter('http://example.com/', r))
    self.assertFalse(domain_filter('test.com', r))

  def test_specific_domain_filter(self):
    r = Response('', LinkCrawlRequest('http://example.com/'))
    f = create_domains_filter(['example2.com', 'example.com'])
    self.assertTrue(f('http://example.com/', r))
    self.assertTrue(f('http://example2.com/', r))
    self.assertFalse(f('http://test.com/', r))


if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestFilters)
  unittest.TextTestRunner(verbosity=2).run(suite)