from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):
    FINISH_BUTTON = (By.ID, "finish")

    def is_loaded(self):
        return self.is_visible((By.CLASS_NAME, "checkout_summary_container"))

    def finish_order(self):
        self.js_click(self.FINISH_BUTTON)
