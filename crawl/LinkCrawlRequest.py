
class LinkCrawlRequest:

  def __init__(self, link, crawl_id = '0', depth = 0):
    self.link = link
    self.attempts = 0
    self.crawl_id = crawl_id
    self.depth = depth

  def addAttempt(self):
    self.attempts += 1

