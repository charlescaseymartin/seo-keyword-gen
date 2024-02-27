from selenium.webdriver import Firefox

class AnswerThePublic:
  browser: Firefox
  keywords: list[str]
  
  def __init__(self, browser: Firefox, keywords: list[str]) -> None:
    self.browser = browser
    self.keywords = keywords
    self.browser.get()
    pass