"""
  Module which contains set implementations for use by crawlers to
  store crawl state.
"""

from .SimpleSet import SimpleSet
from .RedisSet import RedisSet

__all__ = ['SimpleSet', 'RedisSet']