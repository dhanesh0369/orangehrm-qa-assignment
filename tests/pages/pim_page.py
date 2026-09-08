"""
PIM (Employee Management) Page Object - OrangeHRM
Handles Add Employee, Employee List, and employee management operations.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from .base_page import BasePage
import time


class PIMPage(BasePage):
    """Page Object for OrangeHRM PIM Module."""

    # ─── Navigation Locators ─────────────────────────────────────────────────
    ADD_EMPLOYEE_BTN    = (By.XPATH, "//a[normalize-space()='Add Employee']")
    EMPLOYEE_LIST_BTN   = (By.XPATH, "//a[normalize-space()='Employee List']")

    # ─── Add Employee Form ────────────────────────────────────────────────────
    FIRST_NAME_INPUT    = (By.CSS_SELECTOR, "input[name='firstName']")
    MIDDLE_NAME_INPUT   = (By.CSS_SELECTOR, "input[name='middleName']")
    LAST_NAME_INPUT     = (By.CSS_SELECTOR, "input[name='lastName']")
    EMPLOYEE_ID_INPUT   = (By.XPATH, "//label[text()='Employee Id']/following::input[1]")
    SAVE_BTN            = (By.CSS_SELECTOR, "button[type='submit']")

    # ─── Employee List – Search ───────────────────────────────────────────────
    # NOTE: The Employee Name field is an AUTOCOMPLETE widget.
    # We use the plain Search button without name filter to list all employees,
    # then scan row text to find the target employee.
    SEARCH_BTN          = (By.CSS_SELECTOR, "button[type='submit']")

    # ─── Employee List – Table ────────────────────────────────────────────────
    # Each row in the results table; row text contains the full employee name
    EMPLOYEE_TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
    # Loading spinner / "No Records Found" indicator
    SPINNER             = (By.CSS_SELECTOR, ".oxd-loading-spinner")
    NO_RECORDS          = (By.XPATH, "//*[contains(text(),'No Records Found')]")

    # ─── Delete ───────────────────────────────────────────────────────────────
    DELETE_BTN          = (By.CSS_SELECTOR, ".oxd-icon.bi-trash")
    CONFIRM_DELETE_BTN  = (By.CSS_SELECTOR, ".oxd-button--label-danger")

    # ─── Success Toast ────────────────────────────────────────────────────────
    SUCCESS_TOAST       = (By.CSS_SELECTOR, ".oxd-toast--success")

    # ─── Navigation ──────────────────────────────────────────────────────────

    def click_add_employee(self):
        """Navigate to the Add Employee form."""
        self.click(self.ADD_EMPLOYEE_BTN)
        return self

    def click_employee_list(self):
        """Navigate to Employee List page."""
        self.click(self.EMPLOYEE_LIST_BTN)
        return self

    # ─── Add Employee ─────────────────────────────────────────────────────────

    def add_employee(self, first_name, middle_name, last_name):
        """
        Fill and submit the Add Employee form.
        Returns the Employee ID auto-generated on the form.
        """
        # Wait for form to load
        self.find_element(self.FIRST_NAME_INPUT)

        # Fill name fields
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.MIDDLE_NAME_INPUT, middle_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)

        # Capture the auto-generated Employee ID before submitting
        emp_id_element = self.find_element(self.EMPLOYEE_ID_INPUT)
        emp_id = emp_id_element.get_attribute("value")

        # Submit the form
        self.click(self.SAVE_BTN)

        # Wait for redirect away from the save page
        WebDriverWait(self.driver, 20).until(
            lambda d: "saveEmployee" not in d.current_url
        )
        time.sleep(1)

        print(f"✅ Employee added: {first_name} {middle_name} {last_name} (ID: {emp_id})")
        return emp_id

    # ─── Employee List Helpers ────────────────────────────────────────────────

    def _wait_for_table_to_load(self, timeout=10):
        """Wait for the loading spinner to disappear and rows to appear."""
        # Wait for spinner to go away
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.SPINNER)
            )
        except TimeoutException:
            pass

        # Give the table a moment to render
        time.sleep(1.5)

    def search_all_employees(self):
        """
        Click Search with no filters applied.
        This returns ALL employees in the system — we then scan rows manually.
        Avoids the autocomplete complication entirely.
        """
        self._wait_for_table_to_load()
        self.click(self.SEARCH_BTN)
        self._wait_for_table_to_load()

    def get_all_row_texts(self):
        """Return the text content of every visible row in the employee table."""
        try:
            rows = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.EMPLOYEE_TABLE_ROWS)
            )
            texts = []
            for row in rows:
                try:
                    texts.append(row.text.strip())
                except StaleElementReferenceException:
                    pass
            return texts
        except TimeoutException:
            return []

    def verify_employee_in_list(self, first_name, last_name):
        """
        Load ALL employees (empty search) then scan every row's text.
        Prints "Name Verified" if found.
        Returns True/False.
        """
        # Search with no filter to show all employees
        self.search_all_employees()

        row_texts = self.get_all_row_texts()

        for row_text in row_texts:
            if first_name.lower() in row_text.lower() and last_name.lower() in row_text.lower():
                print(f"Name Verified: {first_name} {last_name}")
                return True

        # If not on first page yet, scroll through rows
        rows = self.driver.find_elements(*self.EMPLOYEE_TABLE_ROWS)
        for row in rows:
            self.scroll_to_element(row)
            time.sleep(0.1)
            try:
                row_text = row.text.strip()
                if first_name.lower() in row_text.lower() and last_name.lower() in row_text.lower():
                    print(f"Name Verified: {first_name} {last_name}")
                    return True
            except StaleElementReferenceException:
                pass

        print(f"❌ Employee '{first_name} {last_name}' NOT found in the list.")
        return False

    # ─── Delete ───────────────────────────────────────────────────────────────

    def delete_employee(self, row_index=0):
        """Delete an employee from the list by row index."""
        delete_buttons = self.driver.find_elements(*self.DELETE_BTN)
        if row_index < len(delete_buttons):
            delete_buttons[row_index].click()
            self.click(self.CONFIRM_DELETE_BTN)
            time.sleep(1)
            return True
        return False
