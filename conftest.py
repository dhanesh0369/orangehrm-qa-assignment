"""
conftest.py - Pytest Fixtures for OrangeHRM Test Suite
Shared fixtures used across all test modules.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# ─── Pytest Configuration ────────────────────────────────────────────────────

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "negative: mark test as negative/edge case")


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver():
    """
    Spin up a Chrome WebDriver for each test function.
    Tears down (quits) automatically after the test.
    """
    chrome_options = Options()
    # Uncomment for headless CI/CD:
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """
    Provide a driver that is already logged in to OrangeHRM.
    Used by tests that don't need to test the login step itself.
    """
    from tests.pages.login_page import LoginPage
    login = LoginPage(driver)
    login.open().login("Admin", "admin123")
    return driver
