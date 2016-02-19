
class SimpleSet:

  def __init__(self):
    self.set = set()

  def add(self, x):
    self.set.add(hash(x))

  def __contains__(self, x):
    return hash(x) in self.set
