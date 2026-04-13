# SauceDemo Automation Framework

This repository contains a Python + Selenium automation framework for the SauceDemo case study.

## Setup

1. Install Python 3.11+.
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run tests

- Run the login smoke test:

  ```bash
  pytest -m smoke
  ```

- Run regression tests:

  ```bash
  pytest -m regression
  ```

- Run the full suite:

  ```bash
  pytest
  ```

- Generated HTML report is written to `reports/report.html` when tests run.

## Automated test cases

### Smoke test coverage

- `tests/test_login.py::test_login_success`
- Verifies that a valid standard user can log in successfully and reach the inventory page.
- This is the primary fast sanity check for the build.

### Regression test coverage

- `tests/test_login.py`
  - Valid login
  - Invalid password
  - Missing password
  - Missing username
  - Username length boundary validation
- `tests/test_cart_checkout.py`
  - Add item to cart and verify cart badge and button state
  - Checkout page validation for first name, last name, and postal code
  - Full checkout flow through overview and order completion
  - Cart detail visibility for selected items
  - Logout and unauthorized access redirect behavior

### JMeter performance testing

- The load test plan is located at `performance/jmx/saucedemo_weekend_lab.jmx`.
- Run the JMeter plan with:
  ```bash
  jmeter -n -t performance/jmx/saucedemo_weekend_lab.jmx -l performance/results/results.jtl -e -o performance/html_report
  ```
- After running, view generated performance reports in `performance/html_report`.
- Summary results are available in `performance/results/aggregate.csv` and `performance/Findings.md`.

## Project structure

- `pages/` - Page Object Model classes
  - `base_page.py` contains reusable Selenium helpers, explicit wait wrappers, and common page actions.
  - Individual page classes such as `login_page.py`, `inventory_page.py`, `cart_page.py`, `checkout_info_page.py`, `checkout_overview_page.py`, and `checkout_complete_page.py` encapsulate element locators and user flows for each page.
- `tests/` - Test modules
  - `test_login.py` covers authentication flows, positive login and validation scenarios.
  - `test_cart_checkout.py` covers shopping cart actions, checkout form validation, order completion, and logout/redirect behavior.
- `testdata/` - Data-driven test data files
  - CSV files store input and expected result data for parameterized tests.
  - Separating test data from code makes it easier to maintain and expand test coverage.
- `reports/screenshots/` - Failure screenshots
- `reports/logs/` - Execution logs
- `performance/` - Performance test artifacts

## Performance testing

- `performance/jmx/saucedemo_weekend_lab.jmx` contains the JMeter load test plan.
- Run the load test with JMeter:
  ```bash
  jmeter -n -t performance/jmx/saucedemo_weekend_lab.jmx -l performance/results/results.jtl -e -o performance/html_report
  ```
- `performance/results/aggregate.csv` contains computed response summary metrics.
- `performance/Findings.md` summarizes current results and SPA routing limitations.
