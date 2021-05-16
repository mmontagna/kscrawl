from crawl.http.Abstract import AbstractHttp
from crawl.http.Response import Response
import urllib2

class SimpleHttp(AbstractHttp):

  def get(self, req):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')]
    response = opener.open(req.link, timeout=10)
    return Response(response.read(), req)
