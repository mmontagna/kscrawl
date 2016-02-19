
class AbstractProcessor:

  def process(self, url, response):
    raise NotImplementedError()

  def close(self):
    pass

