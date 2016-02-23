import unittest, boto3
from crawl.processors import S3Store
from crawl.processors import ResponseOutput
from crawl import LinkCrawlRequest
from crawl.http.Response import Response
from mock import MagicMock
import mock
from attrdict import AttrDict

class TestS3Store(unittest.TestCase):

  def make_s3_store(self, buffer_size=100):
    bucket = boto3.resource('s3').Bucket('test')
    obj = AttrDict({'put': MagicMock(return_value=None)})
    bucket.Object = MagicMock(return_value=obj)
    return S3Store('mmontagna-crawl-test', buffer_size=100, s3_bucket_object=bucket), bucket

  def test_X(self):
    store, _ = self.make_s3_store(buffer_size=100)

    resp = Response("<p>This is, a Test.</p>", LinkCrawlRequest('http://example.com/'))
    resp.output.append(ResponseOutput('content', 'pages', {'content' : 'page', 'accessed' : 123}))
    resp.output.append(ResponseOutput('aux', 'index', {'features' : [(1,3),(3,4)], 'accessed' : 123}))
    resp.output.append(ResponseOutput('aux', 'index2', {'features' : [(1,3),(3,4)], 'accessed' : 123}))
    store.process('https://example.com/1', resp)
    store.process('https://example.com/2', resp)



  def test_buffer(self):
    store, bucket = self.make_s3_store(buffer_size=10)

    resp = Response("<p>This is, a Test.</p>", LinkCrawlRequest('http://example.com/'))
    resp.output.append(ResponseOutput('content', 'pages', {'content' : 'page', 'accessed' : 123}))
    resp.output.append(ResponseOutput('content', 'images', {'content' : 'page', 'accessed' : 123}))
    [store.process('https://example.com/1', resp) for i in range(0, 11)]
    store.close()

    bucket.Object.assert_called_with(mock.ANY)
    bucket.Object().put.assert_called_with(Body=mock.ANY)

  def test_close(self):
    store, _ = self.make_s3_store(buffer_size=100)

    resp = Response("<p>This is, a Test.</p>", LinkCrawlRequest('http://example.com/'))
    resp.output.append(ResponseOutput('content', 'pages', {'content' : 'page', 'accessed' : 123}))
    resp.output.append(ResponseOutput('content', 'images', {'content' : 'page', 'accessed' : 123}))
    [store.process('https://example.com/1', resp) for i in range(0, 11)]
    store.close()


if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestS3Store)
  unittest.TextTestRunner(verbosity=2).run(suite)