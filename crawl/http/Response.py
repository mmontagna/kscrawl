from bs4 import BeautifulSoup
import chardet, time

from crawl.processors import ResponseOutput

class Response:
  def __init__(self, raw, request):
    self.raw = raw
    self.encoding = chardet.detect(raw)
    self.content = unicode(raw, self.encoding['encoding'], errors='replace')
    self.request = request
    self.accessed = int(time.time())
    self.output = []
    self.output.append(ResponseOutput('content', 'pages', self.content))

    try:
      self.soup = BeautifulSoup(self.content, "html.parser")
    except:
      pass
