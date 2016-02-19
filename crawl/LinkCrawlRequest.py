
class LinkCrawlRequest:

  def __init__(self, link, crawl_id):
    self.link = link
    self.attempts = 0
    self.crawl_id = crawl_id

  def addAttempt(self):
    self.attempts += 1

