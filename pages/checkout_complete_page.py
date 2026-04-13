from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    COMPLETE_MESSAGE = (By.CLASS_NAME, "complete-header")

    def get_complete_message(self):
        return self.get_text(self.COMPLETE_MESSAGE)

    def is_complete(self):
        return self.is_visible(self.COMPLETE_MESSAGE)
