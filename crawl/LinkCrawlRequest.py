import urlnorm, urlparse

class LinkCrawlRequest:

  def __init__(self, link, parent = None, crawl_id='0'):
    self.link = urlnorm.norm(urlparse.urljoin(parent.link if parent else '', link))
    self.attempts = 0
    self.crawl_id = parent.crawl_id if parent else crawl_id
    self.depth = parent.depth + 1 if parent else 0

  def addAttempt(self):
    self.attempts += 1

  def id(self):
    return self.crawl_id + ':' + self.link

