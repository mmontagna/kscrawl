from crawl.processors.Abstract import AbstractProcessor


class S3OutputStore(AbstractProcessor):
  def __init__(self, bucket):
    self.bucket