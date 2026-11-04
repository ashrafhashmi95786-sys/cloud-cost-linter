Cloud Cost Linter

«A lightweight, privacy-focused Python tool for analyzing cloud billing CSV files, detecting potential duplicate charges, identifying unusual spending, and estimating illustrative cost optimization opportunities.»

""License: MIT" (https://img.shields.io/badge/License-MIT-blue.svg)" (LICENSE)
""Python: 3.7+" (https://img.shields.io/badge/Python-3.7%2B-green.svg)" (https://www.python.org/)

Core Features

- Potential Duplicate Detection: Identifies matching billing entries for manual investigation.
- Cost Anomaly Detection: Detects unusually high spending using statistical analysis.
- Spending Breakdown: Summarizes total spending by cloud service.
- Illustrative Rightsizing Estimates: Provides heuristic cost optimization estimates for selected high-cost entries.
- Local Execution: Designed to process billing files locally.
- Zero Third-Party Python Dependencies: Uses Python standard libraries.

Important Financial Disclaimer

This tool provides analysis and illustrative estimates, not guaranteed savings.

For the included sample billing data:

Category| Amount| Explanation
Illustrative rightsizing estimate| $3,308| Heuristic estimate requiring technical verification
Candidate duplicate charges| $299| Unconfirmed charges requiring provider investigation
Verified savings| $0| No actual savings have been confirmed

These figures represent separate financial categories and must never be combined or described as realized savings.

Rightsizing Estimate Breakdown

- GPU instance: $4,820 × 40% = $1,928
- Storage volume: $3,450 × 40% = $1,380
- Total illustrative rightsizing estimate: $3,308

The 40% reduction is a modeling assumption, not a verified result.

Important Limitations

- Billing records alone cannot determine whether a resource is idle or active.
- Runtime metrics such as CPU, memory and IOPS are needed for resource utilization analysis.
- Matching billing entries may represent legitimate charges.
- Duplicate candidates are not confirmed refunds.
- Actual savings require independent technical and financial verification.

---

Requirements

- Python 3.7 or later
- No third-party Python packages required

Installation

Clone this repository:

git clone https://github.com/ashrafhashmi95786-sys/cloud-cost-linter.git
cd cloud-cost-linter

Alternatively, download the repository ZIP and extract it.

Quick Start

1. Analyze Sample Billing Data

python3 cloud_cost_linter.py sample_billing.csv

2. Generate JSON Output

python3 cloud_cost_linter.py sample_billing.csv --json

3. Adjust Anomaly Sensitivity

python3 cloud_cost_linter.py sample_billing.csv --threshold 1.5

4. Start the Local Web Interface

python3 cloud_cost_linter.py --serve

Alternatively:

python3 cloud_cost_linter_web.py

Open the local address shown by the server in your browser.

The default standalone server address is:

"http://127.0.0.1:8080"

Web Interface Features

- Upload cloud billing CSV files.
- Load sample billing data.
- View spending summaries.
- Review potential duplicate charges.
- Identify unusual spending.
- Export analysis reports as CSV and JSON.

The web interface is intended for local use. Do not expose it to the public internet without an independent security review.

---

Sample Billing Analysis

The included sample dataset contains 20 billing records.

Reported sample analysis:

- Total spending: $11,575.75
- Potential duplicate entries: 2
- Candidate duplicate charges: $299
- Statistical cost outliers: 2
- Illustrative rightsizing estimate: $3,308
- Verified savings: $0

These are sample analysis figures, not guaranteed financial results.

---

CSV File Format

The billing CSV should include these minimum columns:

Column| Description| Example
"record_id"| Unique billing record identifier| "rec_1001"
"service"| Cloud service name| "Compute Engine"
"resource_id"| Resource identifier| "instance-api-01"
"date"| Billing entry date| "2026-10-01"
"cost"| Billing amount| "142.50"

Optional columns may include "region" and "description".

See "sample_billing.csv" for an example.

---

Running Automated Tests

Run the Python test suite:

python3 -m unittest test_cloud_cost_linter.py -v

The development test run reported 28 passing tests.

---

Project Files

- "cloud_cost_linter.py" — Main command-line tool
- "cloud_cost_linter_web.py" — Standalone local web interface
- "sample_billing.csv" — Sample billing dataset
- "test_cloud_cost_linter.py" — Automated Python tests
- "README.md" — Project documentation
- "LICENSE" — MIT License

---

Privacy and Security

- No cloud account credentials are required for CSV analysis.
- The tool is designed for local billing analysis.
- Review billing files before using or sharing them.
- Do not upload passwords, API keys, credentials or private customer information.
- Perform an independent security review before processing sensitive financial data or exposing the web interface to other networks.

---

Contributions

Suggestions, bug reports and improvements are welcome through GitHub Issues and Pull Requests.

License

This project is released under the MIT License. See "LICENSE" (LICENSE) for details.

---

Cloud Cost Linter — Analyze spending. Find anomalies. Make informed decisions.
