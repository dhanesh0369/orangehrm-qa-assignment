"""
Login Page Object - OrangeHRM
Handles all interactions with the Login Page.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Page Object for OrangeHRM Login Page."""

    # ─── Locators ────────────────────────────────────────────────────────────
    USERNAME_INPUT    = (By.CSS_SELECTOR, "input[name='username']")
    PASSWORD_INPUT    = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_BUTTON      = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE     = (By.CSS_SELECTOR, ".oxd-alert-content-text")
    BRAND_LOGO        = (By.CSS_SELECTOR, ".orangehrm-login-logo img")
    FORGOT_PASSWORD   = (By.CSS_SELECTOR, ".orangehrm-login-forgot > p")
    DEMO_CREDENTIALS  = (By.CSS_SELECTOR, ".orangehrm-demo-credentials")
    PAGE_TITLE        = (By.CSS_SELECTOR, ".orangehrm-login-title")

    URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    def open(self):
        """Navigate to the login page."""
        self.driver.get(self.URL)
        self.wait_for_page_load()
        return self

    def enter_username(self, username):
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username, password):
        """Full login sequence."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self):
        """Return the error alert text shown on failed login."""
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def is_error_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)

    def is_logo_visible(self):
        return self.is_element_visible(self.BRAND_LOGO)

    def is_forgot_password_visible(self):
        return self.is_element_visible(self.FORGOT_PASSWORD)

    def click_forgot_password(self):
        self.click(self.FORGOT_PASSWORD)
        return self

    def are_demo_credentials_shown(self):
        return self.is_element_visible(self.DEMO_CREDENTIALS)

    def get_demo_credentials_text(self):
        return self.get_text(self.DEMO_CREDENTIALS)
