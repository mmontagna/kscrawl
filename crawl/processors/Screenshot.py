from crawl.processors.Abstract import AbstractProcessor
from crawl.processors import ResponseOutput
import os, time, uuid, re
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ScreenShot(AbstractProcessor):
  def __init__(self):
    self.driver = webdriver.Remote(
      command_executor=os.environ['SELENIUM_SERVER'],
      desired_capabilities=DesiredCapabilities.FIREFOX)

    self.driver.set_page_load_timeout(8)

  def process(self, crawlRequest, response):
    if ('screenshot' in crawlRequest.options and crawlRequest.options['screenshot']):
      #All we can do is wait.
      self.driver.maximize_window()
      self.driver.get(crawlRequest.link)
      time.sleep(2)
      screenshot = self.driver.get_screenshot_as_png()

      filename = re.sub(r'\W+', '', crawlRequest.link) + '.png'
      if (screenshot):
        response.output.append(ResponseOutput('screenshots', filename, screenshot, raw=True))
        response.output.append(ResponseOutput('screenshots_index', 'screenshots', filename))

  def close(self):
    pass
