# Performance Findings

## Test environment

- JMeter version: 5.6.3
- Test plan: `performance/jmx/saucedemo_weekend_lab.jmx`
- Results file: `performance/results/results.jtl`
- Aggregate summary: `performance/results/aggregate.csv`
- HTML dashboard: `performance/html_report/index.html`

## NFR summary

| NFR ID | Threshold                         | Result | Notes                                                                                    |
| ------ | --------------------------------- | ------ | ---------------------------------------------------------------------------------------- |
| NFR-01 | Login page P95 < 3.0 seconds      | Pass   | Measured P95 = 242 ms for `Login Page` requests.                                         |
| NFR-02 | App shell asset P95 < 4.0 seconds | Fail   | Measured P95 = 5.94 seconds for `App Shell` asset requests.                              |
| NFR-03 | Overall error rate < 2%           | Pass   | Measured error rate = 0.00% across all requests after switching to valid HTTP endpoints. |

## Notes

- The current JMeter test plan issues HTTP GET requests to `/` and `/static/js/main.bcf4bc5f.js`.
- Login page requests were successful and performed well under load.
- The SauceDemo product page is rendered via client-side routing; `/inventory.html` is not a server-rendered endpoint and returns 404 when requested directly.
- This updated test plan validates the home page and app shell asset load performance for a meaningful HTTP-level load test.
- The `App Shell` asset is a 667 KB JavaScript bundle, and its P95 measured 5.94 seconds under the configured 20-user load.
- A more complete SPA load test would require a browser-driven tool that executes client-side routing and localStorage-based login state.
