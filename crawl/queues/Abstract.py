
class AbstractQueue:

  def __iter__(self):
    return self

  def next(self):
    v = self.get()
    if (v):
      return v
    raise StopIteration

  def send(self, links):
    raise NotImplementedError()

  def get(self):
    raise NotImplementedError()

