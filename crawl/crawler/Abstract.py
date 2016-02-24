
class AbstractCrawler():

  def __init__(self, queue, urlset, http):
    if ("send" not in dir(queue) or "get" not in dir(queue)):
      raise Exception('AbstractCrawler: ' + str(queue) + ' must support get & send.')
    if ("add" not in dir(urlset) or "__contains__" not in dir(urlset)):
      raise Exception('AbstractCrawler: ' + str(urlset) + ' must support add & __contains__.')

    self.queue = queue
    self.urlset = urlset
    self.throttle_control = None
    self.http = http
    self.processors = []

  def add_response_processor(self, processor):
    self.processors.append(processor)

  def process(self, url, response):
    for processor in self.processors:
      processor.process(url, response)

  def tick(self):
    for processor in self.processors:
      processor.tick()

  def close(self):
    for processor in self.processors:
      processor.close()
