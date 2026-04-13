# import logging
# from pathlib import Path
# import pytest
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# LOG_DIR = Path("reports/logs")
# SCREENSHOT_DIR = Path("reports/screenshots")
# LOG_DIR.mkdir(parents=True, exist_ok=True)
# SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


# def _configure_logger():
#     logger = logging.getLogger("automation")
#     logger.setLevel(logging.INFO)
#     if not logger.handlers:
#         fh = logging.FileHandler(LOG_DIR / "test_run.log", encoding="utf-8")
#         formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s - %(message)s")
#         fh.setFormatter(formatter)
#         logger.addHandler(fh)
#     return logger


# @pytest.fixture(scope="session")
# def config():
#     return {
#         "base_url": "https://www.saucedemo.com/",
#         "username": "standard_user",
#         "password": "secret_sauce",
#     }


# @pytest.fixture(scope="function")
# def driver(request):
#     logger = _configure_logger()
#     options = Options()
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver.implicitly_wait(5)
#     request.node.driver = driver
#     logger.info(f"Starting browser for {request.node.name}")
#     yield driver
#     outcome = getattr(request.node, "rep_call", None)
#     if outcome is not None and outcome.failed:
#         screenshot_path = SCREENSHOT_DIR / f"{request.node.name}.png"
#         try:
#             driver.save_screenshot(str(screenshot_path))
#             logger.info(f"Saved failure screenshot: {screenshot_path}")
#         except Exception as screenshot_error:
#             logger.error(f"Screenshot capture failed: {screenshot_error}")
#     logger.info(f"Tearing down browser for {request.node.name}")
#     try:
#         driver.quit()
#     except Exception as quit_error:
#         logger.error(f"Error quitting browser: {quit_error}")


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()
#     if report.when == "call":
#         item.rep_call = report
#     return report



import logging
import os
from pathlib import Path
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Directories
LOG_DIR = Path("reports/logs")
SCREENSHOT_DIR = Path("reports/screenshots")
LOG_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def get_local_chromedriver() -> str | None:
    env_path = os.getenv("CHROMEDRIVER_PATH")
    if env_path:
        candidate = Path(env_path).expanduser()
        if candidate.exists():
            return str(candidate)

    cache_dir = Path.home() / ".wdm" / "drivers" / "chromedriver" / "mac64"
    if not cache_dir.exists():
        return None

    for version_dir in sorted(cache_dir.iterdir(), reverse=True):
        if not version_dir.is_dir():
            continue
        for candidate in version_dir.rglob("chromedriver"):
            if candidate.is_file():
                return str(candidate)
    return None


# ✅ Configure logger (session-level)
@pytest.fixture(scope="session")
def logger():
    logger = logging.getLogger("automation")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        log_file = LOG_DIR / "test_run.log"
        fh = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


# ✅ Config fixture
@pytest.fixture(scope="session")
def config():
    return {
        "base_url": "https://www.saucedemo.com/",
        "username": "standard_user",
        "password": "secret_sauce",
    }


# ✅ Driver fixture
@pytest.fixture(scope="function")
def driver(request, logger):
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # 🔥 Optional: headless mode (uncomment if needed)
    # options.add_argument("--headless=new")

    local_driver = get_local_chromedriver()
    if local_driver:
        service = Service(local_driver)
    else:
        service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    request.node.driver = driver
    logger.info(f"🚀 Starting test: {request.node.name}")

    yield driver

    # ✅ Screenshot on failure
    outcome = getattr(request.node, "rep_call", None)
    if outcome and outcome.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = SCREENSHOT_DIR / f"{request.node.name}_{timestamp}.png"

        try:
            driver.save_screenshot(str(screenshot_path))
            logger.error(f"❌ Test failed. Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.error(f"⚠️ Screenshot failed: {e}")

    logger.info(f"🛑 Ending test: {request.node.name}")

    try:
        driver.quit()
    except Exception as e:
        logger.error(f"Error quitting browser: {e}")


# ✅ Hook to capture test result
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.rep_call = report