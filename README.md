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

## Project structure

- `pages/` - Page Object Model classes
- `tests/` - Test modules
- `testdata/` - Data-driven test data files
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
