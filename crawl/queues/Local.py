from crawl.queues.Abstract import AbstractQueue

class LocalQueue(AbstractQueue):

  def __init__(self):
    self.queue = []

  def send(self, links):
    [self.queue.append(link) for link in links]

  def get(self):
    if len(self.queue) > 0:
      return self.queue.pop()
    return None