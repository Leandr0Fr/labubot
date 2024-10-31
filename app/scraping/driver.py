from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._driver = cls._initialize_driver()
        return cls._instance

    @staticmethod
    def _initialize_driver():
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        return driver

    @classmethod
    def get_driver(cls):
        return cls()._driver

    def close_driver(self):
        self._driver.quit()
