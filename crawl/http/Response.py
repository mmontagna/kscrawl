from bs4 import BeautifulSoup
import chardet, time

from crawl.processors import ResponseOutput

class Response:
  def __init__(self, raw, request):
    self.raw = raw
    self.encoding = chardet.detect(raw)
    if (self.encoding['encoding']):
      encoding = self.encoding['encoding']
    else:
      encoding = 'ascii'
    self.content = unicode(raw, encoding, errors='replace')
    self.request = request
    self.accessed = int(time.time())
    self.output = []
    self.output.append(ResponseOutput('content', 'pages', self.content))

    try:
      self.soup = BeautifulSoup(self.content, "html.parser")
    except:
      pass
