from crawl.http.Abstract import AbstractHttp
from crawl.http.Response import Response
import urllib2

class SimpleHttp(AbstractHttp):

  def get(self, req):
    response = urllib2.urlopen(req.link, timeout=10)
    return Response(response.read(), req)