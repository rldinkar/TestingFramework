from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_BANNER = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open(self, base_url):
        super().open(base_url)

    def login(self, username, password):
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_BANNER)

    def is_login_successful(self):
        return self.is_visible((By.CLASS_NAME, "inventory_list"))

    def is_login_page(self):
        return self.is_visible(self.USERNAME)
