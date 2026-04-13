from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def is_loaded(self):
        return self.is_visible(self.CART_ITEMS)

    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
