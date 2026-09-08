"""
Test Suite: Login Functionality - OrangeHRM
Covers 10 test cases (TC_LOGIN_001 through TC_LOGIN_010)
Includes: positive, negative, edge case, and UI validation tests.
"""

import pytest
import time
from tests.pages.login_page import LoginPage
from tests.pages.dashboard_page import DashboardPage


# ─── Constants ───────────────────────────────────────────────────────────────
VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"
BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"


# ─── Test Class ──────────────────────────────────────────────────────────────

class TestLoginFunctionality:
    """
    ═══════════════════════════════════════════════════════════════════════
    TC_LOGIN_001 – TC_LOGIN_010 : Login Page Test Cases
    ═══════════════════════════════════════════════════════════════════════
    """

    # ── TC_LOGIN_001: Valid Login ──────────────────────────────────────────

    @pytest.mark.smoke
    def test_TC_LOGIN_001_valid_login(self, driver):
        """
        TC_LOGIN_001 - Valid Login with Correct Credentials
        Steps:
          1. Navigate to login page.
          2. Enter username: 'Admin'
          3. Enter password: 'admin123'
          4. Click Login button.
        Expected: User is redirected to the Dashboard page.
        """
        login = LoginPage(driver)
        login.open().login(VALID_USERNAME, VALID_PASSWORD)

        dashboard = DashboardPage(driver)
        assert dashboard.is_logged_in(), \
            "TC_LOGIN_001 FAILED: User was not redirected to dashboard after valid login."
        assert dashboard.is_on_dashboard(), \
            "TC_LOGIN_001 FAILED: Dashboard URL not detected."
        print("TC_LOGIN_001 PASSED ✅ - Valid login successful.")

    # ── TC_LOGIN_002: Invalid Username ────────────────────────────────────

    @pytest.mark.negative
    def test_TC_LOGIN_002_invalid_username(self, driver):
        """
        TC_LOGIN_002 - Login with Invalid Username
        Steps:
          1. Navigate to login page.
          2. Enter username: 'wronguser'
          3. Enter password: 'admin123'
          4. Click Login button.
        Expected: Error message is displayed. User stays on login page.
        """
        login = LoginPage(driver)
        login.open().login("wronguser", VALID_PASSWORD)

        assert login.is_error_displayed(), \
            "TC_LOGIN_002 FAILED: No error message shown for invalid username."
        error_text = login.get_error_message()
        assert "invalid" in error_text.lower() or "credentials" in error_text.lower(), \
            f"TC_LOGIN_002 FAILED: Unexpected error message: '{error_text}'"
        assert "login" in driver.current_url.lower(), \
            "TC_LOGIN_002 FAILED: User was redirected away from login page."
        print(f"TC_LOGIN_002 PASSED ✅ - Error shown: '{error_text}'")

    # ── TC_LOGIN_003: Invalid Password ───────────────────────────────────

    @pytest.mark.negative
    def test_TC_LOGIN_003_invalid_password(self, driver):
        """
        TC_LOGIN_003 - Login with Invalid Password
        Steps:
          1. Navigate to login page.
          2. Enter username: 'Admin'
          3. Enter password: 'wrongpassword'
          4. Click Login button.
        Expected: Error message is displayed. User stays on login page.
        """
        login = LoginPage(driver)
        login.open().login(VALID_USERNAME, "wrongpassword")

        assert login.is_error_displayed(), \
            "TC_LOGIN_003 FAILED: No error message shown for wrong password."
        print(f"TC_LOGIN_003 PASSED ✅ - Error correctly shown for wrong password.")

    # ── TC_LOGIN_004: Empty Username ──────────────────────────────────────

    @pytest.mark.negative
    def test_TC_LOGIN_004_empty_username(self, driver):
        """
        TC_LOGIN_004 - Login with Empty Username Field
        Steps:
          1. Navigate to login page.
          2. Leave username field empty.
          3. Enter password: 'admin123'
          4. Click Login button.
        Expected: Validation error shown for username field. Login does not proceed.
        """
        login = LoginPage(driver)
        login.open()
        login.enter_password(VALID_PASSWORD)
        login.click_login()

        assert login.is_error_displayed() or "login" in driver.current_url.lower(), \
            "TC_LOGIN_004 FAILED: No validation shown for empty username."
        print("TC_LOGIN_004 PASSED ✅ - Validation shown for empty username.")

    # ── TC_LOGIN_005: Empty Password ──────────────────────────────────────

    @pytest.mark.negative
    def test_TC_LOGIN_005_empty_password(self, driver):
        """
        TC_LOGIN_005 - Login with Empty Password Field
        Steps:
          1. Navigate to login page.
          2. Enter username: 'Admin'
          3. Leave password field empty.
          4. Click Login button.
        Expected: Validation error shown for password field. Login does not proceed.
        """
        login = LoginPage(driver)
        login.open()
        login.enter_username(VALID_USERNAME)
        login.click_login()

        assert login.is_error_displayed() or "login" in driver.current_url.lower(), \
            "TC_LOGIN_005 FAILED: No validation shown for empty password."
        print("TC_LOGIN_005 PASSED ✅ - Validation shown for empty password.")

    # ── TC_LOGIN_006: Both Fields Empty ──────────────────────────────────

    @pytest.mark.negative
    def test_TC_LOGIN_006_both_fields_empty(self, driver):
        """
        TC_LOGIN_006 - Login with Both Fields Empty
        Steps:
          1. Navigate to login page.
          2. Leave both username and password empty.
          3. Click Login button.
        Expected: Validation errors shown for both fields.
        """
        login = LoginPage(driver)
        login.open()
        login.click_login()

        assert login.is_error_displayed() or "login" in driver.current_url.lower(), \
            "TC_LOGIN_006 FAILED: No validation shown when both fields are empty."
        print("TC_LOGIN_006 PASSED ✅ - Validation shown for empty fields.")

    # ── TC_LOGIN_007: SQL Injection ───────────────────────────────────────

    @pytest.mark.negative
    def test_TC_LOGIN_007_sql_injection(self, driver):
        """
        TC_LOGIN_007 - SQL Injection in Username Field
        Steps:
          1. Navigate to login page.
          2. Enter username: "' OR '1'='1"
          3. Enter password: "' OR '1'='1"
          4. Click Login button.
        Expected: Login is rejected. Application does not crash. Error shown.
        """
        login = LoginPage(driver)
        login.open().login("' OR '1'='1", "' OR '1'='1")

        assert "login" in driver.current_url.lower() or login.is_error_displayed(), \
            "TC_LOGIN_007 FAILED: SQL injection may have bypassed login!"
        print("TC_LOGIN_007 PASSED ✅ - SQL injection correctly rejected.")

    # ── TC_LOGIN_008: Case Sensitivity Check ─────────────────────────────

    @pytest.mark.negative
    def test_TC_LOGIN_008_case_sensitivity(self, driver):
        """
        TC_LOGIN_008 - Login with Wrong Case for Password
        Steps:
          1. Navigate to login page.
          2. Enter username: 'Admin'
          3. Enter password: 'ADMIN123' (uppercase)
          4. Click Login button.
        Expected: Login is rejected (password is case-sensitive). Error shown.
        """
        login = LoginPage(driver)
        login.open().login(VALID_USERNAME, "ADMIN123")

        assert login.is_error_displayed(), \
            "TC_LOGIN_008 FAILED: Case-insensitive password accepted - security risk!"
        print("TC_LOGIN_008 PASSED ✅ - Password correctly treated as case-sensitive.")

    # ── TC_LOGIN_009: Special Characters in Fields ────────────────────────

    @pytest.mark.negative
    def test_TC_LOGIN_009_special_characters(self, driver):
        """
        TC_LOGIN_009 - Login with Special Characters in Fields
        Steps:
          1. Navigate to login page.
          2. Enter username: '!@#$%^&*()'
          3. Enter password: '!@#$%^&*()'
          4. Click Login button.
        Expected: Login is rejected gracefully. No application errors or crashes.
        """
        login = LoginPage(driver)
        login.open().login("!@#$%^&*()", "!@#$%^&*()")

        assert "login" in driver.current_url.lower() or login.is_error_displayed(), \
            "TC_LOGIN_009 FAILED: Special characters caused unexpected behavior."
        print("TC_LOGIN_009 PASSED ✅ - Special characters handled gracefully.")

    # ── TC_LOGIN_010: Forgot Password Link ───────────────────────────────

    @pytest.mark.smoke
    def test_TC_LOGIN_010_forgot_password_link(self, driver):
        """
        TC_LOGIN_010 - Forgot Password Link Navigates Correctly
        Steps:
          1. Navigate to login page.
          2. Click on "Forgot your password?" link.
        Expected: User is redirected to the password reset page.
        """
        login = LoginPage(driver)
        login.open()

        assert login.is_forgot_password_visible(), \
            "TC_LOGIN_010 FAILED: Forgot password link not visible."
        login.click_forgot_password()
        time.sleep(2)

        assert "requestPasswordResetCode" in driver.current_url or \
               "forgot" in driver.current_url.lower(), \
            f"TC_LOGIN_010 FAILED: Unexpected URL: {driver.current_url}"
        print("TC_LOGIN_010 PASSED ✅ - Forgot password page loaded successfully.")

    # ── TC_LOGIN_011: Logout and Session Invalidation ─────────────────────

    @pytest.mark.smoke
    def test_TC_LOGIN_011_logout_invalidates_session(self, driver):
        """
        TC_LOGIN_011 - Successful Logout Redirects to Login Page
        Steps:
          1. Login with valid credentials.
          2. Click on user dropdown → Logout.
        Expected: User is redirected back to the login page.
        """
        login = LoginPage(driver)
        login.open().login(VALID_USERNAME, VALID_PASSWORD)

        dashboard = DashboardPage(driver)
        assert dashboard.is_logged_in(), "Pre-condition failed: Login did not succeed."
        dashboard.logout()

        time.sleep(2)
        assert "login" in driver.current_url.lower(), \
            "TC_LOGIN_011 FAILED: Logout did not redirect to login page."
        print("TC_LOGIN_011 PASSED ✅ - Logout redirects back to login page.")

    # ── TC_LOGIN_012: UI Elements Visible ─────────────────────────────────

    @pytest.mark.smoke
    def test_TC_LOGIN_012_ui_elements_visible(self, driver):
        """
        TC_LOGIN_012 - All UI Elements Are Visible on Login Page
        Steps:
          1. Navigate to login page.
        Expected: Logo, Username field, Password field, Login button, and
                  Forgot password link are all visible.
        """
        login = LoginPage(driver)
        login.open()

        assert login.is_logo_visible(), \
            "TC_LOGIN_012 FAILED: Brand logo not visible."
        assert login.is_element_visible(login.USERNAME_INPUT), \
            "TC_LOGIN_012 FAILED: Username input not visible."
        assert login.is_element_visible(login.PASSWORD_INPUT), \
            "TC_LOGIN_012 FAILED: Password input not visible."
        assert login.is_element_visible(login.LOGIN_BUTTON), \
            "TC_LOGIN_012 FAILED: Login button not visible."
        assert login.is_forgot_password_visible(), \
            "TC_LOGIN_012 FAILED: Forgot password link not visible."
        print("TC_LOGIN_012 PASSED ✅ - All UI elements visible on login page.")
