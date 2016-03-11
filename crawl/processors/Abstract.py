
class AbstractProcessor:

  def process(self, crawlRequest, response):
    raise NotImplementedError()

  def tick(self):
    pass

  def close(self):
    pass

