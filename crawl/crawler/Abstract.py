
class AbstractCrawler():

  def __init__(self, queue, urlset, http, processor):
    if ("send" not in dir(queue) or "get" not in dir(queue)):
      raise Exception('AbstractCrawler: ' + str(queue) + ' must support get & send.')
    if ("add" not in dir(urlset) or "__contains__" not in dir(urlset)):
      raise Exception('AbstractCrawler: ' + str(urlset) + ' must support add & __contains__.')

    self.queue = queue
    self.urlset = urlset
    self.http = http
    self.processor = processor