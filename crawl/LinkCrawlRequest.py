import urlnorm, urlparse, re

class LinkCrawlRequest:

  def __init__(self, link, parent = None, crawl_id='0', depth_limit=float('+inf'),
    accept=None, output_prefix='crawl', bucket=None, options = {}):
    try:
      self.link = urlnorm.norm(urlparse.urljoin(parent.link if parent else '', link))
      self.link = self.link.split('#')[0]
    except:
      self.link = ''
    self.attempts = 0
    self.crawl_id = parent.crawl_id if parent else crawl_id
    self.depth = parent.depth + 1 if parent else 0
    self.depth_limit = parent.depth_limit if parent else depth_limit
    self.accept = parent.accept if parent else accept
    self.output_prefix = parent.output_prefix if parent else output_prefix
    self.output_bucket = parent.output_bucket if parent else bucket
    self.options = parent.options if parent else options

  def follow(self, parent):
    return self.link != '' and self.depth < self.depth_limit and (self.accept is None or self.accept(self.link, parent))

  def addAttempt(self):
    self.attempts += 1

  def id(self):
    return self.crawl_id + ':' + self.link

  def __eq__(self, other):
      if isinstance(other, self.__class__):
          return ((self.link == other.link) and (self.crawl_id == other.crawl_id))
      else:
          return False
def domain_filter(next_url, parent_response):
  try:
    return urlparse.urlparse(next_url).netloc == urlparse.urlparse(parent_response.request.link).netloc
  except:
    return False

def create_domains_filter(domains):
  def _h(next_url, parent_response):
    try:
      return urlparse.urlparse(next_url).netloc in domains
    except:
      return False
  return _h