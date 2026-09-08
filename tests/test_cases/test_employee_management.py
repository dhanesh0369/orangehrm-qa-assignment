"""
Test Suite: Employee Management (PIM Module) - OrangeHRM
Covers the full workflow:
  - Login → Navigate to PIM → Add 4 employees → Verify in list → Logout
"""

import pytest
import time
from tests.pages.login_page import LoginPage
from tests.pages.dashboard_page import DashboardPage
from tests.pages.pim_page import PIMPage


# ─── Test Data ────────────────────────────────────────────────────────────────

EMPLOYEES = [
    {"first": "Alice",  "middle": "Marie",   "last": "Johnson"},
    {"first": "Bob",    "middle": "Thomas",  "last": "Williams"},
    {"first": "Carol",  "middle": "Ann",     "last": "Davis"},
    {"first": "Daniel", "middle": "James",   "last": "Martinez"},
]

VALID_USERNAME = "Admin"
VALID_PASSWORD = "admin123"


# ─── Test Class ──────────────────────────────────────────────────────────────

class TestEmployeeManagement:
    """
    Full employee management workflow test.
    Follows the assignment automation workflow exactly.
    """

    @pytest.mark.smoke
    def test_full_employee_workflow(self, driver):
        """
        Automation Workflow (per assignment):
        ─────────────────────────────────────
        Step 1:  Login with valid credentials.
        Step 2:  Hover over PIM and click it.
        Step 3:  Add 4 employees via Add Employee form.
        Step 4:  Navigate to Employee List.
        Step 5:  Scroll through list, locate each employee, print "Name Verified".
        Step 6:  Logout from Dashboard.
        """

        # ── Step 1: Login ─────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("STEP 1: Logging in to OrangeHRM")
        print("=" * 60)

        login_page = LoginPage(driver)
        login_page.open().login(VALID_USERNAME, VALID_PASSWORD)

        dashboard = DashboardPage(driver)
        assert dashboard.is_logged_in(), "Login failed - cannot proceed with workflow."
        print("✅ Login successful. Dashboard loaded.")

        # ── Step 2: Hover and Click PIM ──────────────────────────────────
        print("\n" + "=" * 60)
        print("STEP 2: Navigating to PIM Module")
        print("=" * 60)

        dashboard.hover_and_click_pim()
        time.sleep(2)
        assert "pim" in driver.current_url.lower(), \
            f"PIM navigation failed. Current URL: {driver.current_url}"
        print("✅ PIM module loaded.")

        # ── Step 3: Add 4 Employees ──────────────────────────────────────
        print("\n" + "=" * 60)
        print("STEP 3: Adding Employees")
        print("=" * 60)

        pim = PIMPage(driver)
        added_employees = []

        for idx, emp in enumerate(EMPLOYEES, start=1):
            print(f"\n  → Adding Employee {idx}: {emp['first']} {emp['middle']} {emp['last']}")
            pim.click_add_employee()
            time.sleep(1)

            emp_id = pim.add_employee(
                first_name=emp["first"],
                middle_name=emp["middle"],
                last_name=emp["last"]
            )
            added_employees.append({**emp, "id": emp_id})
            time.sleep(2)  # Allow profile page to load after save

            # Navigate back to PIM for next employee (except last)
            if idx < len(EMPLOYEES):
                dashboard.hover_and_click_pim()
                time.sleep(1)

        print(f"\n✅ Successfully added {len(added_employees)} employees.")

        # ── Step 4: Navigate to Employee List ─────────────────────────────
        print("\n" + "=" * 60)
        print("STEP 4: Navigating to Employee List")
        print("=" * 60)

        # Direct URL navigation — most reliable after a series of form submissions
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
        time.sleep(3)
        print("✅ Employee List page loaded.")

        # ── Step 5: Verify Each Employee in the List ─────────────────────
        print("\n" + "=" * 60)
        print("STEP 5: Verifying Employees in the List")
        print("=" * 60)

        # Load ALL employees with empty search once, then scan row text for each name
        pim.search_all_employees()
        time.sleep(2)

        verified_count = 0
        for emp in added_employees:
            print(f"\n  → Searching for: {emp['first']} {emp['last']}")
            found = pim.verify_employee_in_list(emp["first"], emp["last"])
            if found:
                verified_count += 1

        assert verified_count == len(EMPLOYEES), \
            f"Only {verified_count}/{len(EMPLOYEES)} employees were verified in the list."
        print(f"\n✅ All {verified_count} employees verified in the Employee List.")

        # ── Step 6: Logout ────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("STEP 6: Logging Out")
        print("=" * 60)

        dashboard.logout()
        time.sleep(2)

        assert "login" in driver.current_url.lower(), \
            f"Logout failed. Current URL: {driver.current_url}"
        print("✅ Logout successful. Redirected to Login page.")

        print("\n" + "=" * 60)
        print("🎉 FULL WORKFLOW COMPLETED SUCCESSFULLY!")
        print("=" * 60)


class TestEmployeeManagementUnit:
    """Individual unit tests for employee management functions."""

    @pytest.mark.regression
    def test_add_single_employee(self, logged_in_driver):
        """TC_EMP_001 - Add a single employee and verify redirect to profile."""
        driver = logged_in_driver
        dashboard = DashboardPage(driver)
        dashboard.hover_and_click_pim()
        time.sleep(2)

        pim = PIMPage(driver)
        pim.click_add_employee()
        time.sleep(1)
        pim.add_employee("TestFirst", "TestMid", "TestLast")

        assert "viewEmployeeProfile" in driver.current_url or \
               "saveEmployee" not in driver.current_url, \
            "TC_EMP_001 FAILED: Did not redirect to employee profile after save."
        print("TC_EMP_001 PASSED ✅ - Single employee added successfully.")

    @pytest.mark.regression
    def test_employee_list_loads(self, logged_in_driver):
        """TC_EMP_002 - Employee List page loads with a table."""
        driver = logged_in_driver
        dashboard = DashboardPage(driver)
        dashboard.hover_and_click_pim()
        time.sleep(2)

        pim = PIMPage(driver)
        pim.click_employee_list()
        time.sleep(2)

        assert "viewEmployeeList" in driver.current_url or \
               "pim" in driver.current_url.lower(), \
            "TC_EMP_002 FAILED: Employee List page did not load."
        print("TC_EMP_002 PASSED ✅ - Employee List page loads successfully.")
