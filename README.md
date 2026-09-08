# OrangeHRM QA Assignment 2026

Automated test suite for the OrangeHRM demo application using **Python + Selenium + Pytest** following the **Page Object Model (POM)** design pattern.

> **Live App:** https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
> **Credentials (demo):** `Admin` / `admin123`

---

## Project Structure

```
orangehrm-qa-assignment/
├── conftest.py                      ← Pytest fixtures (WebDriver setup/teardown)
├── pytest.ini                       ← Pytest config + HTML report settings
├── requirements.txt                 ← Python dependencies
├── tests/
│   ├── pages/                       ← Page Object Model classes
│   │   ├── base_page.py             ← Shared utilities (wait, click, type, etc.)
│   │   ├── login_page.py            ← Login page interactions
│   │   ├── dashboard_page.py        ← Dashboard navigation & logout
│   │   └── pim_page.py              ← PIM module (add/search/verify/delete employees)
│   └── test_cases/
│       ├── test_login.py            ← 12 login test cases (TC_LOGIN_001–012)
│       └── test_employee_management.py  ← Full employee workflow automation
└── reports/                         ← Auto-generated HTML reports (gitignored)
```

---

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Google Chrome (latest)
- ChromeDriver (auto-managed by `webdriver-manager`)

### 2. Clone and Install

```bash
git clone <your-repo-url>
cd orangehrm-qa-assignment
pip install -r requirements.txt
```

### 3. Run Tests

```bash
# Run ALL tests
pytest

# Run only smoke tests
pytest -m smoke -v

# Run only login tests
pytest tests/test_cases/test_login.py -v

# Run the full automation workflow (add employees, verify, logout)
pytest tests/test_cases/test_employee_management.py::TestEmployeeManagement -v

# Run negative/edge case tests
pytest -m negative -v
```

HTML reports are auto-generated at `reports/test_report.html` after each run.

---

## Automation Workflow (Assignment Requirement)

The `test_full_employee_workflow` test executes the exact workflow specified in the assignment:

| Step | Action | Implementation |
|------|--------|----------------|
| 1 | Login | `LoginPage.open().login("Admin", "admin123")` |
| 2 | Hover & click PIM | `DashboardPage.hover_and_click_pim()` |
| 3 | Add 4 employees | `PIMPage.add_employee(first, middle, last)` × 4 |
| 4 | Go to Employee List | `PIMPage.click_employee_list()` |
| 5 | Verify names | `PIMPage.verify_employee_in_list(fn, ln)` → prints `"Name Verified"` |
| 6 | Logout | `DashboardPage.logout()` |

### Employees Added in Tests

| # | First | Middle | Last |
|---|-------|--------|------|
| 1 | Alice | Marie | Johnson |
| 2 | Bob | Thomas | Williams |
| 3 | Carol | Ann | Davis |
| 4 | Daniel | James | Martinez |

---

## Test Cases Summary

### Login Tests (`test_login.py`)

| TC ID | Scenario | Type |
|-------|----------|------|
| TC_LOGIN_001 | Valid login with correct credentials | Smoke ✅ |
| TC_LOGIN_002 | Invalid username | Negative ❌ |
| TC_LOGIN_003 | Invalid password | Negative ❌ |
| TC_LOGIN_004 | Empty username field | Negative ❌ |
| TC_LOGIN_005 | Empty password field | Negative ❌ |
| TC_LOGIN_006 | Both fields empty | Negative ❌ |
| TC_LOGIN_007 | SQL injection in credentials | Security 🔒 |
| TC_LOGIN_008 | Password case sensitivity | Security 🔒 |
| TC_LOGIN_009 | Special characters in fields | Edge Case ⚠️ |
| TC_LOGIN_010 | Forgot password link navigation | Smoke ✅ |
| TC_LOGIN_011 | Logout and session invalidation | Smoke ✅ |
| TC_LOGIN_012 | UI elements visibility check | UI 🖥️ |

### Employee Management Tests (`test_employee_management.py`)

| Test | Scenario |
|------|----------|
| `test_full_employee_workflow` | End-to-end: Login → Add 4 employees → Verify in list → Logout |
| `test_add_single_employee` | Unit: Add one employee and verify profile redirect |
| `test_employee_list_loads` | Unit: Employee List page loads correctly |

---

## Identified Bugs

| Bug ID | Title | Severity |
|--------|-------|----------|
| BUG_001 | Demo credentials exposed in plain text on login page | Medium |
| BUG_002 | No account lockout after repeated failed login attempts | High 🔴 |
| BUG_003 | No show/hide password toggle on password field | Low |

See the full [QA Assignment Document](../brain/c2f9ffa1-361c-468f-b03a-cb46c3d9d894/qa_assignment_document.md) for detailed write-ups.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Test scripting language |
| Selenium 4 | Browser automation |
| Pytest 8 | Test framework and runner |
| pytest-html | HTML test report generation |
| webdriver-manager | Automatic ChromeDriver management |

---

## Design Patterns Used

- **Page Object Model (POM)** — UI interactions encapsulated in page classes
- **Fixture-based setup** — `driver` and `logged_in_driver` fixtures in `conftest.py`
- **Explicit Waits** — `WebDriverWait` over `time.sleep` for robust synchronization
- **Pytest Markers** — `smoke`, `regression`, `negative` for selective test runs
