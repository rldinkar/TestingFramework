from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def js_click(self, locator):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)
        return element

    def type_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator):
        element = self.find(locator)
        return element.text

    def is_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)) is not None
        except TimeoutException:
            return False
