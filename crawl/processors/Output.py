
class ResponseOutput():
  def __init__(self, folder, name,
    content, raw=False):
    self.folder = folder
    self.name = name
    self.content = content
    self.raw = raw