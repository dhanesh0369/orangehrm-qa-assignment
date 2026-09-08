"""
Dashboard Page Object - OrangeHRM
Handles interactions with the Dashboard and top nav.
"""

from selenium.webdriver.common.by import By
from .base_page import BasePage
import time


class DashboardPage(BasePage):
    """Page Object for OrangeHRM Dashboard."""

    # ─── Locators ────────────────────────────────────────────────────────────
    DASHBOARD_TITLE   = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6")
    USER_DROPDOWN     = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LOGOUT_OPTION     = (By.XPATH, "//a[text()='Logout']")
    PIM_MENU          = (By.XPATH, "//span[text()='PIM']")
    NAV_MENU_ITEMS    = (By.CSS_SELECTOR, ".oxd-main-menu-item--name")

    def is_on_dashboard(self):
        """Verify we are on the dashboard by checking URL."""
        return "dashboard" in self.get_current_url()

    def get_dashboard_title(self):
        return self.get_text(self.DASHBOARD_TITLE)

    def hover_and_click_pim(self):
        """Hover over PIM menu item and click it."""
        self.hover(self.PIM_MENU)
        time.sleep(0.5)
        self.click(self.PIM_MENU)
        return self

    def logout(self):
        """Click user dropdown and select Logout."""
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_OPTION)
        return self

    def is_logged_in(self):
        """Check if user dropdown is visible (indicates logged in state)."""
        return self.is_element_visible(self.USER_DROPDOWN, timeout=10)
