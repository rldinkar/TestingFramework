from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, timeout=20, poll_frequency=0.5):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout, poll_frequency=poll_frequency)

    def open(self, url):
        self.driver.get(url)
        self.wait_for_page_load()

    def wait_for_page_load(self):
        return self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def wait_for_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find(self, locator):
        return self.wait_for_visible(locator)

    def click(self, locator):
        element = self.wait_for_clickable(locator)
        element.click()
        return element

    def js_click(self, locator):
        element = self.wait_for_visible(locator)
        self.driver.execute_script("arguments[0].click();", element)
        return element

    def type_text(self, locator, text):
        element = self.wait_for_visible(locator)
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator):
        element = self.wait_for_visible(locator)
        return element.text

    def wait_for_text(self, locator, text):
        return self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_url_contains(self, string):
        return self.wait.until(EC.url_contains(string))

    def is_visible(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)) is not None
        except TimeoutException:
            return False
