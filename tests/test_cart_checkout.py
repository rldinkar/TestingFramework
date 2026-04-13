import csv
from pathlib import Path
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage


def login_standard_user(driver, config):
    login_page = LoginPage(driver)
    login_page.open(config["base_url"])
    login_page.login(config["username"], config["password"])
    assert login_page.is_login_successful(), "Login should succeed for standard_user"
    return InventoryPage(driver)


def begin_checkout(driver, config):
    inventory_page = login_standard_user(driver, config)
    inventory_page.click_first_product_button()
    inventory_page.navigate_to_cart()
    cart_page = CartPage(driver)
    cart_page.click_checkout()
    return CheckoutInfoPage(driver)


def load_checkout_data():
    rows = []
    path = Path(__file__).resolve().parent.parent / "testdata" / "checkout_data.csv"
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(
                (
                    row["first_name"],
                    row["last_name"],
                    row["postal_code"],
                    row["should_succeed"].strip().lower() == "true",
                    row["error_message"],
                )
            )
    return rows


@pytest.mark.smoke
def test_add_to_cart_updates_badge_and_button(driver, config):
    inventory_page = login_standard_user(driver, config)
    assert inventory_page.get_cart_count() == 0
    assert inventory_page.get_first_product_button_label().lower() == "add to cart"

    inventory_page.click_first_product_button()
    assert inventory_page.get_cart_count() == 1
    assert inventory_page.get_first_product_button_label().lower() == "remove"

    inventory_page.navigate_to_cart()
    cart_page = CartPage(driver)
    assert cart_page.is_loaded(), "Cart page should show the added item"


@pytest.mark.regression
def test_checkout_first_name_is_required(driver, config):
    inventory_page = login_standard_user(driver, config)
    inventory_page.click_first_product_button()
    inventory_page.navigate_to_cart()

    cart_page = CartPage(driver)
    cart_page.click_checkout()

    checkout_info = CheckoutInfoPage(driver)
    checkout_info.fill_information("", "Test", "12345")
    assert "First Name is required" in checkout_info.get_error_message()


@pytest.mark.regression
@pytest.mark.parametrize("first_name,last_name,postal_code,should_succeed,error_message", load_checkout_data())
def test_checkout_information_validation(driver, config, first_name, last_name, postal_code, should_succeed, error_message):
    inventory_page = login_standard_user(driver, config)
    inventory_page.click_first_product_button()
    inventory_page.navigate_to_cart()

    cart_page = CartPage(driver)
    cart_page.click_checkout()

    checkout_info = CheckoutInfoPage(driver)
    checkout_info.fill_information(first_name, last_name, postal_code)

    if should_succeed:
        overview_page = CheckoutOverviewPage(driver)
        assert overview_page.is_loaded(), "Checkout overview should load when inputs are valid"
        overview_page.finish_order()
        complete_page = CheckoutCompletePage(driver)
        assert complete_page.is_complete(), "Order completion should show success message"
    else:
        assert error_message in checkout_info.get_error_message()


@pytest.mark.regression
def test_remove_item_from_cart_updates_badge_and_button(driver, config):
    inventory_page = login_standard_user(driver, config)
    inventory_page.click_first_product_button()
    assert inventory_page.get_cart_count() == 1

    inventory_page.click_first_product_button()
    assert inventory_page.get_cart_count() == 0
    assert inventory_page.get_first_product_button_label().lower() == "add to cart"


@pytest.mark.regression
def test_checkout_postal_code_is_required(driver, config):
    checkout_info = begin_checkout(driver, config)
    checkout_info.fill_information("Test", "Test", "")
    assert "Postal Code is required" in checkout_info.get_error_message()


@pytest.mark.regression
def test_checkout_last_name_is_required(driver, config):
    checkout_info = begin_checkout(driver, config)
    checkout_info.fill_information("Test", "", "12345")
    assert "Last Name is required" in checkout_info.get_error_message()


@pytest.mark.regression
def test_checkout_overview_loads_with_valid_information(driver, config):
    checkout_info = begin_checkout(driver, config)
    checkout_info.fill_information("Test", "Test", "12345")
    overview_page = CheckoutOverviewPage(driver)
    assert overview_page.is_loaded(), "Checkout overview should load when valid information is provided"


@pytest.mark.regression
def test_cart_page_shows_selected_item_details(driver, config):
    inventory_page = login_standard_user(driver, config)
    inventory_page.click_first_product_button()
    inventory_page.navigate_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.is_loaded(), "Cart page should show selected items"
    assert "Sauce Labs Backpack" in driver.page_source or "Sauce Labs" in driver.page_source


@pytest.mark.regression
def test_finish_order_shows_success_message(driver, config):
    inventory_page = login_standard_user(driver, config)
    inventory_page.click_first_product_button()
    inventory_page.navigate_to_cart()

    cart_page = CartPage(driver)
    cart_page.click_checkout()

    checkout_info = CheckoutInfoPage(driver)
    checkout_info.fill_information("Test", "Test", "12345")

    overview_page = CheckoutOverviewPage(driver)
    assert overview_page.is_loaded(), "Checkout overview should load with valid information"
    overview_page.finish_order()

    complete_page = CheckoutCompletePage(driver)
    assert complete_page.is_complete(), "Order completion should show success message"
    assert "Thank you" in complete_page.get_complete_message()


@pytest.mark.regression
def test_unauthorized_access_redirects_to_login_after_logout(driver, config):
    inventory_page = login_standard_user(driver, config)
    inventory_page.logout()

    driver.get(config["base_url"] + "inventory.html")
    login_page = LoginPage(driver)
    assert login_page.is_login_page(), "Logout should redirect access to inventory page back to login"


