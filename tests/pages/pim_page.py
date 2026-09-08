"""
PIM (Employee Management) Page Object - OrangeHRM
Handles Add Employee, Employee List, and employee management operations.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

    # ─── Employee List ────────────────────────────────────────────────────────
    SEARCH_NAME_INPUT   = (By.XPATH, "//label[text()='Employee Name']/following::input[1]")
    SEARCH_BTN          = (By.CSS_SELECTOR, "button[type='submit']")
    EMPLOYEE_TABLE_ROWS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row")
    EMPLOYEE_NAME_CELLS = (By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row .oxd-table-cell:nth-child(3)")
    NO_RECORDS_FOUND    = (By.CSS_SELECTOR, ".oxd-text--span")
    DELETE_BTN          = (By.CSS_SELECTOR, ".oxd-icon.bi-trash")
    CONFIRM_DELETE_BTN  = (By.CSS_SELECTOR, ".oxd-button--label-danger")

    # ─── Success Toast ────────────────────────────────────────────────────────
    SUCCESS_TOAST       = (By.CSS_SELECTOR, ".oxd-toast--success")

    def click_add_employee(self):
        """Navigate to the Add Employee form."""
        self.click(self.ADD_EMPLOYEE_BTN)
        return self

    def click_employee_list(self):
        """Navigate to Employee List page."""
        self.click(self.EMPLOYEE_LIST_BTN)
        return self

    def add_employee(self, first_name, middle_name, last_name):
        """
        Fill and submit the Add Employee form.
        Returns the Employee ID auto-generated on the form.
        """
        # Wait for form to load
        self.find_element(self.FIRST_NAME_INPUT)

        # Clear and fill name fields
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.MIDDLE_NAME_INPUT, middle_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)

        # Capture the auto-generated Employee ID
        emp_id_element = self.find_element(self.EMPLOYEE_ID_INPUT)
        emp_id = emp_id_element.get_attribute("value")

        # Submit
        self.click(self.SAVE_BTN)

        # Wait for success toast or redirect
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SUCCESS_TOAST)
            )
        except TimeoutException:
            pass  # Some versions redirect directly

        # Wait for redirect to employee profile
        WebDriverWait(self.driver, 15).until(
            lambda d: "viewEmployeeProfile" in d.current_url or
                      "saveEmployee" not in d.current_url
        )

        print(f"✅ Employee added: {first_name} {middle_name} {last_name} (ID: {emp_id})")
        return emp_id

    def search_employee_by_name(self, name):
        """Search for an employee by name in the Employee List."""
        search_input = self.find_element(self.SEARCH_NAME_INPUT)
        search_input.clear()
        search_input.send_keys(name)
        time.sleep(1)  # Allow autocomplete to populate

        self.click(self.SEARCH_BTN)
        time.sleep(2)  # Wait for results to load

    def get_employee_names_in_list(self):
        """Return a list of employee full names from the table."""
        try:
            cells = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.EMPLOYEE_NAME_CELLS)
            )
            return [cell.text.strip() for cell in cells if cell.text.strip()]
        except TimeoutException:
            return []

    def verify_employee_in_list(self, first_name, last_name):
        """
        Scroll through the employee list and verify the employee exists.
        Prints "Name Verified" when found.
        """
        full_name = f"{first_name} {last_name}"
        self.search_employee_by_name(full_name)

        names = self.get_employee_names_in_list()
        for name in names:
            if first_name.lower() in name.lower() and last_name.lower() in name.lower():
                print(f"Name Verified: {name}")
                return True

        print(f"❌ Employee '{full_name}' NOT found in the list.")
        return False

    def scroll_and_find_employee(self, first_name, last_name):
        """Scroll through all pages to locate the employee."""
        rows = self.driver.find_elements(*self.EMPLOYEE_TABLE_ROWS)
        for row in rows:
            self.scroll_to_element(row)
            time.sleep(0.2)
            row_text = row.text
            if first_name.lower() in row_text.lower() and last_name.lower() in row_text.lower():
                print(f"Name Verified: {first_name} {last_name}")
                return True
        return False

    def delete_employee(self, row_index=0):
        """Delete an employee from the list by row index."""
        delete_buttons = self.driver.find_elements(*self.DELETE_BTN)
        if row_index < len(delete_buttons):
            delete_buttons[row_index].click()
            self.click(self.CONFIRM_DELETE_BTN)
            time.sleep(1)
            return True
        return False
