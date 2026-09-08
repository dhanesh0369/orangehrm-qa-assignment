"""
Base Page - OrangeHRM POM Framework
Contains shared utilities for all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class BasePage:
    """Base class for all Page Objects."""

    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
        self.actions = ActionChains(driver)

    def find_element(self, locator):
        """Wait for element to be visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator):
        """Wait for element to be clickable and return it."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        """Click an element after waiting for it to be clickable."""
        element = self.find_clickable(locator)
        element.click()
        return element

    def type_text(self, locator, text):
        """Clear and type text into an input field."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Get the text content of an element."""
        return self.find_element(locator).text

    def is_element_visible(self, locator, timeout=5):
        """Check if an element is visible within a timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def hover(self, locator):
        """Hover over an element."""
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()

    def scroll_to_element(self, element):
        """Scroll to bring an element into view."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)

    def wait_for_page_load(self, timeout=10):
        """Wait until document.readyState is complete."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def get_current_url(self):
        return self.driver.current_url

    def take_screenshot(self, name="screenshot"):
        """Save a screenshot with a timestamp."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path = f"reports/{name}_{timestamp}.png"
        self.driver.save_screenshot(path)
        return path
