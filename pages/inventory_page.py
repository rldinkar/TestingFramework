from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    PRODUCT_LIST = (By.CLASS_NAME, "inventory_list")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    FIRST_PRODUCT_BUTTON = (By.CSS_SELECTOR, ".inventory_item:first-child button")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def is_loaded(self):
        return self.is_visible(self.PRODUCT_LIST)

    def get_cart_count(self):
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def get_first_product_button_label(self):
        return self.get_text(self.FIRST_PRODUCT_BUTTON)

    def click_first_product_button(self):
        return self.click(self.FIRST_PRODUCT_BUTTON)

    def navigate_to_cart(self):
        self.click(self.CART_LINK)

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.js_click(self.LOGOUT_LINK)
