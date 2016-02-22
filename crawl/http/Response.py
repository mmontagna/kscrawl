from bs4 import BeautifulSoup
import chardet, time

class Response:
  def __init__(self, raw, request):
    self.raw = raw
    self.encoding = chardet.detect(raw)
    self.content = unicode(raw, self.encoding['encoding'])
    self.request = request
    self.accessed = int(time.time())
    self.output = []
    try:
      self.soup = BeautifulSoup(self.content, "html.parser")
    except:
      pass