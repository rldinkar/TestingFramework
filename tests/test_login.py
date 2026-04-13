import csv
from pathlib import Path
import pytest
from pages.login_page import LoginPage


def load_login_data():
    rows = []
    path = Path(__file__).resolve().parent.parent / "testdata" / "login_data.csv"
    with open(path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(
                (
                    row["username"],
                    row["password"],
                    row["should_succeed"].strip().lower() == "true",
                    row["error_message"],
                )
            )
    return rows


@pytest.mark.smoke
def test_login_success(driver, config):
    login_page = LoginPage(driver)
    login_page.open(config["base_url"])
    login_page.login(config["username"], config["password"])
    assert login_page.is_login_successful(), "Expected to reach inventory page after valid login"


@pytest.mark.regression
@pytest.mark.parametrize("username,password,should_succeed,error_message", load_login_data())
def test_login_validation(driver, config, username, password, should_succeed, error_message):
    login_page = LoginPage(driver)
    login_page.open(config["base_url"])
    login_page.login(username, password)
    if should_succeed:
        assert login_page.is_login_successful()
    else:
        assert error_message in login_page.get_error_message()


@pytest.mark.regression
def test_login_failure_blank_username(driver, config):
    login_page = LoginPage(driver)
    login_page.open(config["base_url"])
    login_page.login("", config["password"])
    assert "Epic sadface: Username is required" in login_page.get_error_message()


@pytest.mark.regression
def test_login_failure_username_length_exceeds_boundary(driver, config):
    login_page = LoginPage(driver)
    login_page.open(config["base_url"])
    long_username = "user_" + "a" * 31
    login_page.login(long_username, config["password"])
    assert "Epic sadface: Username and password do not match any user in this service" in login_page.get_error_message()


