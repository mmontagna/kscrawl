from crawl.crawler import AbstractCrawler

from BeautifulSoup import BeautifulSoup
from crawl.LinkCrawlRequest import LinkCrawlRequest
import urlnorm, urlparse


class SimpleCrawler(AbstractCrawler):
  limit = 20

  def crawl(self):
    try:
      while True:
        if (self.limit == 0):
          print 'stopping at limit'
          break
        crawlRequest = self.queue.get()
        if crawlRequest is None:
          break
        try:
          print "Crawling ", crawlRequest.link
          response = self.http.get(crawlRequest)
          self.processor.process(crawlRequest.link, response)
          self.limit -= 1
          soup = BeautifulSoup(response.content)
          for link in soup.findAll('a'):
              if link.get('href'):
                try:
                  #print "link ", link.get('href')
                  link = urlparse.urljoin(crawlRequest.link, link.get('href'))
                  normalized = urlnorm.norm(link)
                  if (normalized not in self.urlset):
                    newRequest = LinkCrawlRequest(normalized, crawlRequest.crawl_id)
                    self.queue.send([newRequest])
                    self.urlset.add(newRequest.link)
                except Exception as e:
                  print "Error", link, e
                  pass

        except Exception as e:
          #Increment attempts and forward this request on
          crawlRequest.addAttempt()
          if (crawlRequest.attempts < 3):
            self.queue.send([crawlRequest])
          print "Error on link - retry",crawlRequest.link, e
    finally:
      self.processor.close()