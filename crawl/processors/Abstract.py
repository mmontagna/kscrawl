
class AbstractProcessor:

  def process(self, url, response):
    raise NotImplementedError()

  def tick(self):
    pass

  def close(self):
    pass

