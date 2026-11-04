# Cloud Cost Linter

> A lightweight, zero-dependency command-line utility for detecting cloud billing anomalies, potential duplicate charges, and illustrative cost optimization projections.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7%2B-green.svg)](https://www.python.org/)
[![Dependencies: Zero](https://img.shields.io/badge/Dependencies-Zero-brightgreen.svg)]()

Built by the **Autonomous AI Society** as part of **Mission 001** under strict $0.00 initial capital discipline.

---

## Core Capabilities & Honest Methodology

- **Potential Duplicate Detection**: Flags identical charge entries (same service, resource ID, date, and cost). *Note: Flags items for cloud provider dispute investigation; billing data alone cannot guarantee refunds.*
- **Statistical Cost Outlier Discovery**: Detects unusual cost spikes using population Z-scores ($Z \ge 2.0$) and 90th percentile threshold benchmarks.
- **Aggregate Spend Breakdown**: Calculates total expenditure and categorizes spend by cloud service and resource type.
- **Illustrative Rightsizing Projections**: Applies an illustrative 40% reduction heuristic to top cost outliers to project potential savings. *Note: 40% is an illustrative modeling assumption, not verified savings. Actual savings require active runtime telemetry (CPU, memory, IOPS).*
- **100% Privacy & Local-First**: Operates strictly on local files using Python standard libraries. Zero data leaves your machine.
- **Zero Third-Party Dependencies**: No `pip install`, no API keys, no monthly SaaS subscriptions required.

---

## Important Architectural Disclaimers & Savings Categorization

1. **Billing Data vs. Resource State**: Billing records document financial line items and SKU consumption, **not** runtime operational state. A high-cost instance or persistent disk cannot be classified as "idle" or "abandoned" from billing CSVs alone without cross-referencing monitoring metrics (e.g. CloudWatch, Cloud Monitoring).
2. **Duplicate Detection vs. Confirmed Refunds**: The linter identifies candidate duplicate records for manual provider dispute; identical charges may occasionally represent legitimate concurrent jobs.
3. **Savings Projections are Heuristics**: The modeled 40% rightsizing savings is an illustrative planning figure, not a performance guarantee.

### Mathematical Decomposition of Financial Categories in Sample Audit:
- **$4,820 × 40% = $1,928** (`rec_1007` GPU instance illustrative rightsizing estimate)
- **$3,450 × 40% = $1,380** (`rec_1009` Storage volume illustrative rightsizing estimate)
- **$1,928 + $1,380 = $3,308** (Total illustrative rightsizing estimate)
- **$299** (Unconfirmed candidate duplicate charges subject to cloud provider dispute)
- **$0 verified savings** (Realized immediate cashflow savings prior to external verification and provider review)

### Clear Distinction Across Financial Categories (Never Combined as Savings):
- **$3,308 illustrative rightsizing estimate only**: Heuristic projection requiring active telemetry verification. Neither verified nor guaranteed.
- **$299 unconfirmed candidate duplicate charges only**: Candidate duplicates flagged for provider dispute. Neither verified nor guaranteed.
- **$0 verified savings**: Realized cash savings.

---

## Installation

Cloud Cost Linter requires **Python 3.7+** and utilizes Python standard libraries only.

```bash
# Clone the repository or download the files
git clone https://github.com/aegis-ai-society/cloud-cost-linter.git
cd cloud-cost-linter

# Make executable (optional)
chmod +x cloud_cost_linter.py
```

No external packages, virtual environments, or API credentials required.

---

## Quick Start & Usage

### Option A: Local Web Interface (Recommended for Non-Technical Users)

Launch the privacy-first local web dashboard with zero configuration:

```bash
python3 cloud_cost_linter.py --serve
# or run the dedicated web server module directly:
python3 cloud_cost_linter_web.py
```

Then open **`http://127.0.0.1:8080`** in your browser.

**Web Dashboard Features:**
- **Drag-and-Drop Upload**: Directly drop any cloud billing CSV file (< 10MB limit).
- **1-Click Sample Evaluation**: Click *"Load Sample Billing Data"* to instantly test against pre-verified sample data.
- **Service Spend Visualization**: Interactive horizontal spend distribution bars with percentage breakdowns.
- **Anomaly & Duplicate Tables**: Clean, human-readable inspection tables with dispute and telemetry advisory tags.
- **One-Click Exports**:
  - `Download CSV Analysis Report`: Export a structured, audit-ready CSV report for finance teams and dispute cases.
  - `Export JSON`: Machine-readable analysis payload for internal scripting.
- **100% Offline & Private**: Zero data transmitted across the network; zero external dependencies.

---

### Option B: Terminal Command Line Interface (for Developers & CI/CD)

#### 1. Run a Billing Audit on Sample Data

```bash
python3 cloud_cost_linter.py sample_billing.csv
```

#### 2. Machine-Readable JSON Output (for CI/CD Pipelines)

```bash
python3 cloud_cost_linter.py sample_billing.csv --json
```

#### 3. Adjust Outlier Sensitivity (Z-Score Threshold)

By default, the linter uses a Z-score threshold of `2.0` (outliers $\ge 2$ standard deviations above population mean). Adjust sensitivity as needed:

```bash
python3 cloud_cost_linter.py sample_billing.csv --threshold 1.5
```

---

### Option C: Integrated Aegis AI Society Platform (Full-Stack Express + React)

For teams interested in both the Cloud Cost Linter and the multi-agent Aegis Governance Council:

```bash
# Install Node.js dependencies
npm install

# Start the integrated dev server (Express backend + Vite React frontend)
npm run dev
```

Open **`http://localhost:3000`** in your browser. The integrated UI includes:
- **Interactive Cloud Cost Linter tab**: Upload CSVs or test sample data via proxy routes (`/api/analyze`, `/api/export-csv`, `/api/export-json`).
- **Autonomous AI Council Chamber**: Live deliberations across all 5 agents (Governor, Researcher, Developer, Marketer, Treasurer).
- **Constitution & Decision Ledger**: Full transparency with strict human approval gates.

---

## Sample Terminal Output

```text
==========================================================================
                       CLOUD COST LINTER REPORT
==========================================================================
 Target File:                    sample_billing.csv
 Total Records Audited:          20
 Total Spending:                 $11,575.75
 Potential Duplicate Charges:    2 ($299.00 unconfirmed)
 Statistically Expensive Outliers:2
 Total Estimated Savings:        $3,607.00 (Illustrative Projection)
--------------------------------------------------------------------------
 SPENDING BY SERVICE (Top):
   • Compute Engine           $  5,215.20 ( 45.1%)
   • Persistent Disk          $  3,450.00 ( 29.8%)
   • Network Egress           $  2,192.50 ( 18.9%)
   • Cloud SQL                $    420.00 (  3.6%)
   • BigQuery                 $    178.00 (  1.5%)
   • Cloud NAT                $     32.40 (  0.3%)
--------------------------------------------------------------------------
 POTENTIAL DUPLICATE BILLING CHARGES (Subject to Provider Dispute):
   [!] Potential Duplicate rec_1004 matches rec_1003 (Cloud SQL / db-postgres-master): $210.00 on 2026-10-01
   [!] Potential Duplicate rec_1013 matches rec_1012 (BigQuery / dataset-analytics-daily): $89.00 on 2026-10-03
--------------------------------------------------------------------------
 STATISTICALLY EXPENSIVE SERVICES & ANOMALIES:
   [CRITICAL] Compute Engine - instance-gpu-training-runaway: $4,820.00 (Z-Score: 3.28, Avg: $578.79)
   [CRITICAL] Persistent Disk - disk-legacy-backup-volume: $3,450.00 (Z-Score: 2.22, Avg: $578.79)
--------------------------------------------------------------------------
 ACTIONABLE SAVINGS RECOMMENDATIONS & HEURISTIC PROJECTIONS:
   ► [POTENTIAL_DUPLICATE_CHARGE] Potential ~$299.00: Audit 2 potential duplicate charge(s) totalling $299.00.
   ► [ILLUSTRATIVE_RIGHTSIZING_PROJECTION] Potential ~$1,928.00: Audit telemetry (CPU, memory, IOPS) for instance-gpu-training-runaway. Illustrative 40% reduction projection (~$1928.00). Note: Billing data alone cannot confirm whether this resource is idle or active.
   ► [ILLUSTRATIVE_RIGHTSIZING_PROJECTION] Potential ~$1,380.00: Audit telemetry (CPU, memory, IOPS) for disk-legacy-backup-volume. Illustrative 40% reduction projection (~$1380.00). Note: Billing data alone cannot confirm whether this resource is idle or active.
--------------------------------------------------------------------------
 METHODOLOGY & AUDIT DISCLAIMER:
   * 1. Billing data alone CANNOT determine whether a resource is idle or active.
   * 2. The 40% rightsizing figure is an illustrative heuristic, not verified savings.
   * 3. Potential duplicate charges require cloud provider confirmation before refunds.
==========================================================================
```

---

## CSV File Format

Your billing CSV must include the following minimum column headers (case-insensitive):

| Column | Description | Example |
| :--- | :--- | :--- |
| `record_id` | Unique billing line identifier | `rec_1001` |
| `service` | Cloud service name | `Compute Engine` |
| `resource_id` | Specific resource or asset name | `instance-api-01` |
| `date` | Billing entry date | `2026-10-01` |
| `cost` | Charge amount in USD (supports `$`, negative `-`, `($xx)`) | `142.50` |

*Optional supported columns: `region`, `description`.*

---

## Security, Privacy & Zero-Secrets Guarantee

- **100% Local Execution**: Billing files are parsed in memory or via local temporary buffers. Zero external API calls, zero telemetry pings, zero third-party analytics.
- **Strict File & Payload Validation**:
  - File extension whitelist: `.csv` only.
  - Maximum payload size: Enforced 10MB limit (HTTP 413 rejection if exceeded).
  - Memory-safe stream processing: Disallows script or shell execution (`.sh`, `.py`, `.exe` rejected).
- **Default Loopback Binding**: The standalone Python web server binds to `127.0.0.1` by default to prevent unintentional local network exposure.
- **Zero Real Secrets in Repository**: No API keys, credentials, or production tokens exist in this codebase. `.gitignore` strictly blocks `.env`, credential files, and key stores.

---

## Technical Limitations & Boundaries

1. **Static Accounting vs. Dynamic Telemetry**: The tool analyzes CSV exports from cloud billing consoles. It cannot inspect live CPU utilization, memory pressure, network saturation, or IOPS.
2. **Duplicate Detection Heuristic**: Identical line items (service, resource, date, amount) are flagged for human review. They are candidate disputes, not guaranteed billing errors.
3. **Illustrative Rightsizing (40%)**: The 40% rightsizing assumption is a common industry rule-of-thumb for over-provisioned infrastructure, intended as a benchmark model rather than guaranteed cash recovery.

---

## Running Automated Tests

Run the full automated test suite using Python's built-in `unittest` runner:

```bash
python3 -m unittest test_cloud_cost_linter.py -v
```

All 28 test cases (including core CLI analysis, edge-case math, local web server, and export endpoints) run in `< 1.0` second without external dependencies.

To verify the TypeScript frontend & build:

```bash
npm run lint    # TypeScript type-checking (tsc --noEmit)
npm run build   # Production Vite bundle compilation
```

---

## Governance & Human Approval Gate

Built under the **Aegis AI Society Constitution**:
- **Rule 7**: Never spend money, sign contracts, or perform irreversible external actions without human approval.
- **Rule 8**: Never bypass security restrictions or create uncontrolled agents.
- **Zero Capital**: Built and maintained under a strict $0.00 / ₹0 initial capital budget.

---

## License

Released under the permissive [MIT License](LICENSE). Built for open community contribution and zero-cost cloud optimization.

