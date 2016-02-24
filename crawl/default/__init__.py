from urlparse import urlparse
import time

def domain_hash(linkCrawlReq):
  dest = 0
  try:
    minute = str(int(time.time()) %  10) # (60*10)
    dest = hash(urlparse(linkCrawlReq.link).netloc + minute + str(linkCrawlReq.attempts))
  except Exception as e:
    print e
    pass
  return dest

def domain_filter(domains):
  from urlparse import urlparse
  domains = domains
  def helper(linkCrawlReq):
    try:
      if urlparse(linkCrawlReq.link).netloc in domains:
        return True
    except:
      pass
    return False
  return helper
