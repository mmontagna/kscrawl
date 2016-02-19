import chardet

class Response:
  def __init__(self, raw, request):
    self.raw = raw
    self.encoding = chardet.detect(raw)
    self.content = unicode(raw, self.encoding['encoding'])
    self.request = request