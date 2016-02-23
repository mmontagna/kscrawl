from crawl.processors.Abstract import AbstractProcessor
from collections import Counter
from sklearn.feature_extraction import FeatureHasher
from crawl.processors import ResponseOutput
import itertools, string, sys, unicodedata

class PageVectorizer(AbstractProcessor):
  tbl = dict.fromkeys(i for i in xrange(sys.maxunicode)
                        if unicodedata.category(unichr(i)).startswith('P'))
  def __init__(self, n_features=100):
    self.hasher = FeatureHasher(n_features=n_features, non_negative=True)

  """
  Args:
    response: A response object
  Returns:
    Array of strings
  """
  def clean_and_filter(self, response):
    [x.extract() for x in response.soup.findAll('script')]
    for tag in response.soup.findAll():
      tag.string = tag.text + ' '
    text = response.soup.get_text().translate(self.tbl)
    text = filter(lambda x: x != '' and not x.isspace(), text.split())
    text = [x.lower() for x in text]
    return text

  """
  Args:
    words: An array of strings
  Returns:
    Vector of index, value tuples eg (x, y, value)
  """
  def feature_vector(self, words):
    bag_of_words = Counter(words)
    feature_vector = self.hasher.transform([bag_of_words])
    x, y = feature_vector.nonzero()
    return [(int(y[i]), int(feature_vector[x[i], y[i]])) for i in range(len(x))]

  def process(self, url, response):
    response.feature_vector = self.feature_vector(self.clean_and_filter(response))

    response.output.append(ResponseOutput('auxiliary', 'feature_hash', response.feature_vector))

  def close(self):
    pass
