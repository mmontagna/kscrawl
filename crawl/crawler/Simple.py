from crawl.crawler import AbstractCrawler

from crawl import LinkCrawlRequest
import urlnorm, urlparse, time


class SimpleCrawler(AbstractCrawler):
  limit = float('nan')
  depth_limit = 20
  _stop_on_empty = False
  retry_limit = 2

  def stop_on_empty(self):
    self._stop_on_empty = True

  def follow(self, response, newRequest):
    return newRequest.id() not in self.urlset and newRequest.depth < self.depth_limit and newRequest.follow(response)
  def crawl(self):
    try:
      while True:
        self.tick()
        if (self.throttle_control):
          time.sleep(self.throttle_control)
        if (self.limit == 0):
          print 'stopping at limit'
          break
        crawlRequest = self.queue.get()
        if crawlRequest is None:
          if self._stop_on_empty:
            print 'Stopping due to empty queue.'
            break
          print "Queue empty sleeping"
          time.sleep(1)
          continue
        try:
          print "Crawling ", crawlRequest.link, 'attempt',crawlRequest.attempts,
          print 'crawl id',crawlRequest.crawl_id, 'depth', crawlRequest.depth
          response = self.http.get(crawlRequest)
          self.limit -= 1

          self.process(crawlRequest.link, response)

          for link in response.soup.findAll('a'):
              if link.get('href'):
                try:
                  newRequest = LinkCrawlRequest(link.get('href'), crawlRequest)
                  if (self.follow(response, newRequest)):
                    self.queue.send([newRequest])
                    self.urlset.add(newRequest.id())
                except Exception as e:
                  print "Error", newRequest.link, link, e

        except Exception as e:
          #Increment attempts and forward this request on
          crawlRequest.addAttempt()
          if (crawlRequest.attempts < self.retry_limit):
            self.queue.send([crawlRequest])
          print "Error on link - retry",crawlRequest.link, e

    finally:
      self.close()
