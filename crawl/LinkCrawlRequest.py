import urlnorm, urlparse, re

class LinkCrawlRequest:

  def __init__(self, link, parent = None, crawl_id='0', depth_limit=float('+inf'), accept=None):
    self.link = urlnorm.norm(urlparse.urljoin(parent.link if parent else '', link))
    self.attempts = 0
    self.crawl_id = parent.crawl_id if parent else crawl_id
    self.depth = parent.depth + 1 if parent else 0
    self.depth_limit = parent.depth_limit if parent else depth_limit
    self.accept = parent.accept if parent else accept

  def follow(self, parent):
    return self.depth < self.depth_limit and (self.accept is None or self.accept(self.link, parent))

  def addAttempt(self):
    self.attempts += 1

  def id(self):
    return self.crawl_id + ':' + self.link


def domain_filter(next_url, parent_response):
  from urlparse import urlparse
  return urlparse(next_url).netloc == urlparse(parent_response.request.link).netloc
