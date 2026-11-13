"""Human-readable public pages and original FinOps guides for Cloud Cost Linter."""
from html import escape

BASE = "https://cloud-cost-linter.onrender.com"

PAGES = {
    "privacy": {
        "title": "Privacy Policy",
        "description": "How Cloud Cost Linter handles uploaded cloud billing CSV files and website information.",
        "heading": "Privacy Policy",
        "updated": "November 13, 2026",
        "body": """
<p>Cloud Cost Linter is a cloud-billing analysis tool. This policy explains what happens when you visit the hosted demo at cloud-cost-linter.onrender.com.</p>
<h2>Billing files you upload</h2>
<p>When you use the hosted demo, the CSV text and the filename you provide are sent over HTTPS to the application server so it can perform the requested analysis and prepare a report. The application processes the submitted billing data in memory and does not intentionally write uploaded CSV contents to persistent application storage.</p>
<p>This statement describes the application's intended handling. The hosting provider may process network, security, diagnostic, or operational metadata under its own policies. Cloud Cost Linter does not control the provider's infrastructure retention practices. Do not upload confidential, regulated, customer-identifying, or otherwise sensitive billing exports.</p>
<h2>Information the website may process</h2>
<p>The service receives the content and filename of a CSV submitted for analysis. The hosting platform may also process technical request information such as IP address, request time, and user-agent information for operating and securing the service. The application does not require an account, password, cloud credentials, or API keys.</p>
<h2>Cookies, analytics, and advertising</h2>
<p>The current hosted application does not intentionally set advertising cookies or include third-party analytics or advertising scripts. Advertising is not currently enabled on this website. If advertising or analytics services are introduced, the website's implementation and this policy will be updated to describe the services actually in use.</p>
<h3>Google AdSense and third-party advertising</h3>
<p>Advertising is not currently enabled on this website. If Google AdSense or another advertising service is enabled in the future, Google and other third-party vendors or ad networks may use cookies and similar technologies to serve and measure ads. These technologies may include cookies, web beacons, device identifiers, IP addresses, and browser information. Third-party vendors, including Google, may use cookies to serve ads based on a user's prior visits to this website or other websites. Google's advertising cookies may allow Google and its partners to serve ads based on visits to this website and/or other websites.</p>
<p>Depending on the advertising service, user settings, and applicable choices, ads may be personalized using activity across websites or may be non-personalized and based on contextual information such as page content and general location. If advertising is introduced, this policy will be updated to identify the vendors and ad networks actually serving ads and link to their relevant privacy and opt-out information. Vendors may collect, receive, or use information under their own privacy policies.</p>
<p>Read <a href="https://policies.google.com/technologies/partner-sites">how Google uses information from sites or apps that use its services</a> and Google's <a href="https://policies.google.com/privacy">Privacy Policy</a>.</p>
<h3>Advertising choices</h3>
<p>When Google personalized advertising is in use, users can review or change available settings through <a href="https://adssettings.google.com/">Google Ads Settings</a>. Users may also visit <a href="https://www.aboutads.info/choices/">YourAdChoices</a> to learn about choices for participating third-party vendors. These controls depend on the vendors, browser, device, and location and may not cover every advertising provider. Browser settings may also allow users to block or delete cookies, although some website or advertising features may not work as intended.</p>
<h3>Consent where required</h3>
<p>Where applicable law or Google's policies require consent, the website operator must provide the required disclosures and obtain and respect the user's choices before using advertising cookies or other local storage, or collecting, sharing, or using personal data for ads personalization. In particular, Google requires publishers using AdSense, Ad Manager, or AdMob to use a Google-certified consent management platform (CMP) integrated with the IAB Europe Transparency and Consent Framework (TCF) when serving personalized ads to users in the European Economic Area (EEA), the United Kingdom, or Switzerland. This certified-CMP requirement is specific to personalized ads in those regions; other consent obligations may still apply depending on the user's location and the advertising configuration. This policy notice does not itself collect consent or replace a required CMP or consent mechanism. See Google's <a href="https://support.google.com/adsense/answer/13554116">publisher CMP requirements for the EEA, UK, and Switzerland</a> and <a href="https://support.google.com/adsense/answer/7670013">CMP setup guidance</a>.</p>
<h2>External services</h2>
<p>The hosted demo runs on Render. Your connection to the hosted website and its infrastructure is subject to the hosting provider's terms and privacy information as well as this application-level notice.</p>
<h2>Your choices and questions</h2>
<p>You can use the local version of the open-source tool to process files on your own computer. For questions or privacy-related requests, contact the project through the <a href="https://github.com/ashrafhashmi95786-sys/cloud-cost-linter/issues">GitHub issue tracker</a>. Do not post private billing data in a public issue.</p>
"""
    },
    "terms": {
        "title": "Terms of Use",
        "description": "Terms and limitations for using the Cloud Cost Linter website and open-source tool.",
        "heading": "Terms of Use",
        "updated": "November 13, 2026",
        "body": """
<p>By using Cloud Cost Linter, you agree to use the service responsibly and to review its output before making operational or financial decisions.</p>
<h2>Purpose of the tool</h2>
<p>Cloud Cost Linter analyzes billing CSV records to summarize spending, flag statistical outliers, identify possible duplicate entries, and show illustrative rightsizing estimates. It is an informational aid, not an accounting service, cloud-provider certification, security audit, or financial advisory service.</p>
<h2>Results require independent verification</h2>
<p>A billing record alone cannot prove that a cloud resource is idle or over-provisioned. Statistical outliers are signals for investigation, not proof of waste. Similar billing rows may be legitimate. Potential duplicate charges are not confirmed overcharges or guaranteed refunds. Rightsizing estimates are illustrative assumptions and are not promised savings.</p>
<h2>Your responsibilities</h2>
<p>You are responsible for checking that you have the right to upload and process any file, reviewing the output, validating findings with your cloud provider and runtime telemetry, and maintaining appropriate backups. Do not upload confidential, regulated, customer-identifying, or sensitive billing data to the public hosted demo.</p>
<h2>Availability and changes</h2>
<p>The hosted demo is provided on an as-available basis. Features, limits, and availability may change. The service may reject malformed files or files exceeding its published upload limit.</p>
<h2>Open-source software</h2>
<p>The project source code is published under the MIT License. The license terms for the source code are separate from these terms governing use of the hosted website.</p>
<h2>No warranty</h2>
<p>To the extent permitted by applicable law, the tool is provided without warranties of accuracy, fitness for a particular purpose, or uninterrupted availability. You must independently verify any decision based on its output.</p>
<h2>Contact</h2>
<p>For questions about these terms, email <a href="mailto:ashwebtools95@gmail.com">ashwebtools95@gmail.com</a>. Do not include passwords, API keys, access tokens, customer details, or confidential billing exports.</p>
"""
    },
    "about": {
        "title": "About Cloud Cost Linter",
        "description": "Learn what Cloud Cost Linter does, how its billing analysis works, and what its results mean.",
        "heading": "About Cloud Cost Linter",
        "updated": "November 13, 2026",
        "body": """
<p>Cloud Cost Linter is a lightweight, open-source utility that helps teams inspect cloud billing exports and decide what deserves a closer look.</p>
<h2>What it helps you review</h2>
<ul>
<li><strong>Spending summaries:</strong> total costs and service-level breakdowns from supported CSV records.</li>
<li><strong>Potential duplicates:</strong> matching entries that may deserve a provider-side investigation.</li>
<li><strong>Cost outliers:</strong> statistical signals that identify unusually expensive records for review.</li>
<li><strong>Illustrative rightsizing:</strong> a clearly labelled estimate to help frame further investigation.</li>
<li><strong>Exportable reports:</strong> CSV and JSON outputs for follow-up analysis.</li>
</ul>
<h2>How it works</h2>
<p>Provide a billing CSV containing the required record identifier, service, resource identifier, date, and cost fields. The tool validates the input, calculates summaries, and presents findings for human review. It does not connect to your cloud account and does not need cloud credentials.</p>
<h2>What it cannot determine</h2>
<p>Billing data does not include all runtime context. It cannot independently confirm whether a resource was idle, whether a repeated charge is erroneous, or whether a projected reduction is achievable. Verify findings using provider invoices, resource configuration, and CPU, memory, storage, or network telemetry.</p>
<h2>Open source</h2>
<p>The project is available on <a href="https://github.com/ashrafhashmi95786-sys/cloud-cost-linter">GitHub</a> under the MIT License. Contributions and issue reports are welcome.</p>
"""
    },
    "contact": {
        "title": "Contact Cloud Cost Linter",
        "description": "How to report a bug, request an improvement, or ask a question about Cloud Cost Linter.",
        "heading": "Contact",
        "updated": "November 13, 2026",
        "body": """
<p>Cloud Cost Linter is an open-source project. For questions, support, bug reports, or feature requests, you can contact the project team by email.</p>
<h2>Email us</h2>
<p><a href="mailto:ashwebtools95@gmail.com">ashwebtools95@gmail.com</a></p>
<p>Please describe the issue clearly. Do not email passwords, API keys, access tokens, customer details, or confidential billing exports.</p>
<h2>Contribute to the project</h2>
<p>Review the <a href="https://github.com/ashrafhashmi95786-sys/cloud-cost-linter">source repository</a> and submit a pull request with a clear description and relevant tests.</p>
<h2>Protect your information</h2>
<p>Never attach passwords, API keys, access tokens, customer details, or private billing exports to a public issue. Share only a small synthetic example that contains no confidential information.</p>
"""
    }
}

GUIDES = {
    "cloud-billing-csv-guide": {
        "title": "How to Read a Cloud Billing CSV: A Practical Guide",
        "description": "A practical guide to cloud billing CSV columns, export checks, cost normalization, and safe analysis.",
        "heading": "How to Read a Cloud Billing CSV",
        "body": """
<p>A cloud billing CSV turns provider charges into rows that can be filtered, grouped, compared, and investigated. It is a useful starting point for FinOps work, but it is not a complete record of resource health or business value. A careful review begins by understanding what each row represents and which billing rules produced it.</p>
<h2>1. Understand the common billing fields</h2>
<p>Provider exports differ, but many contain equivalents of the following fields:</p>
<table><thead><tr><th>Field</th><th>What it usually means</th><th>What to verify</th></tr></thead><tbody>
<tr><td>Record or line-item ID</td><td>Identifier for an individual billing row</td><td>Whether it is stable and unique in this export</td></tr>
<tr><td>Service or product</td><td>Cloud service associated with the charge</td><td>Provider naming and product-family grouping</td></tr>
<tr><td>Resource ID</td><td>Resource associated with usage, when supplied</td><td>Whether IDs are missing, renamed, or scoped to a region</td></tr>
<tr><td>Usage or billing date</td><td>Date or interval represented by the charge</td><td>Timezone, interval boundaries, and billing-period coverage</td></tr>
<tr><td>Cost or amount</td><td>Charge, credit, or adjustment amount</td><td>Currency, sign, tax treatment, and pricing basis</td></tr>
</tbody></table>
<p>Other useful dimensions may include account, project, subscription, region, availability zone, SKU, usage type, quantity, unit, pricing model, tags, and invoice ID. Keep these dimensions when possible: removing them too early can make later investigation difficult.</p>
<h2>2. Check the export before comparing costs</h2>
<p>Before analyzing a file, confirm that it covers the intended billing period and that all expected accounts and services are included. Check whether the export is final or still subject to adjustment. Some providers revise usage, apply credits later, or publish delayed line items.</p>
<ul>
<li><strong>Currency:</strong> do not add amounts in different currencies without a documented conversion method and date.</li>
<li><strong>Taxes and credits:</strong> identify whether totals include tax, discounts, refunds, promotional credits, or support charges.</li>
<li><strong>Commitments:</strong> understand how reservations, savings plans, committed-use discounts, and amortized costs are represented.</li>
<li><strong>Granularity:</strong> hourly, daily, and monthly exports are not directly interchangeable.</li>
<li><strong>Completeness:</strong> compare export totals with the provider invoice or billing console.</li>
</ul>
<h2>3. Normalize carefully</h2>
<p>For a useful comparison, group rows using consistent dimensions such as service, resource, region, and time period. Avoid treating two rows as equivalent merely because their amounts match. A charge may be split across usage types, or several legitimate rows may refer to one resource.</p>
<p>For example, imagine a report contains three storage-related rows for the same resource on one day: storage capacity, request operations, and data retrieval. Those rows may all be valid components of the service. A useful analysis preserves the usage type and unit rather than collapsing everything into one apparent duplicate.</p>
<h2>4. A simple review workflow</h2>
<ol>
<li>Save an unchanged copy of the original export in an approved, access-controlled location.</li>
<li>Record the export date, billing period, currency, provider, and account scope.</li>
<li>Validate required columns and check for blank identifiers, invalid dates, and non-numeric amounts.</li>
<li>Reconcile the total with the provider's billing console or invoice.</li>
<li>Group spending by service, account, project, region, and resource where those dimensions exist.</li>
<li>Investigate large changes using deployment history, usage metrics, and pricing details.</li>
<li>Document findings, assumptions, owners, and follow-up actions.</li>
</ol>
<h2>5. Prepare a file for Cloud Cost Linter</h2>
<p>Cloud Cost Linter's current CSV interface expects these exact column names: <code>record_id</code>, <code>service</code>, <code>resource_id</code>, <code>date</code>, and <code>cost</code>. Map provider-specific column names to this schema in a working copy. Keep the original export unchanged so that you can trace every transformation.</p>
<p>Use a synthetic or non-sensitive sample when trying the <a href="/">Cloud Cost Linter hosted analyzer</a>. The hosted demo sends the selected CSV to its server for temporary in-memory processing. The application does not intentionally save uploaded CSV contents, but hosting infrastructure may process operational metadata. Do not upload confidential, customer-identifying, regulated, or sensitive billing exports.</p>
<h2>6. Common mistakes to avoid</h2>
<ul>
<li>Comparing gross charges in one period with net charges in another.</li>
<li>Mixing currencies or timezones without normalizing them.</li>
<li>Assuming a missing resource ID means the charge is invalid.</li>
<li>Removing credits, taxes, or adjustments without documenting why.</li>
<li>Interpreting billing amounts as proof of utilization or idle capacity.</li>
</ul>
<h2>Further verification</h2>
<p>Use your provider's official billing documentation to confirm field definitions and pricing semantics for the export format you use. A CSV analysis should guide investigation, not replace invoice reconciliation or provider-specific documentation.</p>
"""
    },
    "cloud-billing-anomaly-detection": {
        "title": "Cloud Billing Anomaly Detection: Methods and Investigation",
        "description": "Understand cloud cost anomalies, statistical outliers, baselines, and a repeatable investigation workflow.",
        "heading": "Cloud Billing Anomaly Detection Explained",
        "body": """
<p>A cloud billing anomaly is a cost movement that differs from an expected pattern. It may be caused by a genuine workload change, a deployment, a pricing or discount change, an export issue, or normal seasonality. The purpose of anomaly detection is to identify where investigation may be valuable—not to declare that a charge is wrong.</p>
<h2>1. Define the comparison you want to make</h2>
<p>An anomaly is meaningful only relative to a baseline. Decide whether you are comparing daily spend with recent days, this month with the same month last year, or a resource with its own historical usage. Choose a consistent scope: account, project, service, region, SKU, or resource.</p>
<p>Comparing total company spend can hide a large increase in one small service. Conversely, examining individual line items without grouping can create noisy alerts. Select a level that is useful to the team responsible for investigating it.</p>
<h2>2. Understand common detection approaches</h2>
<h3>Absolute and percentage thresholds</h3>
<p>A rule can flag a cost increase above a fixed amount or percentage. It is simple to explain and useful for known budgets, but a percentage threshold can overreact to small baselines. A change from one unit to two units is a 100% increase even when the financial impact is negligible.</p>
<h3>Rolling averages</h3>
<p>A rolling average compares the current observation with a recent window. It can reveal gradual changes, but may lag when a workload grows steadily. Choose a window long enough to smooth routine noise without hiding meaningful changes.</p>
<h3>Standard deviation and Z-scores</h3>
<p>A Z-score expresses how far an observation is from the mean in units of standard deviation. A large positive score can identify an unusually high value. This approach is easiest to interpret when observations are reasonably stable and the sample is large enough to estimate variation.</p>
<p>Statistical assumptions matter. A few extreme values can distort the mean and standard deviation. Small samples, intermittent workloads, zero-heavy data, and seasonal patterns can make a simple Z-score misleading. A threshold such as 2.0 is a screening rule, not a universal definition of an anomaly.</p>
<h2>3. Investigate a flagged cost change</h2>
<ol>
<li><strong>Validate the data:</strong> confirm the billing period, currency, export completeness, and whether the provider has revised the invoice.</li>
<li><strong>Locate the change:</strong> break the total down by account, service, region, SKU, and resource.</li>
<li><strong>Compare like with like:</strong> use equivalent time windows and account for weekends, month length, and seasonal demand.</li>
<li><strong>Check technical events:</strong> review deployments, autoscaling, data transfers, backups, storage growth, and scheduled jobs.</li>
<li><strong>Check commercial events:</strong> review price changes, discount expiry, commitment coverage, credits, and tax adjustments.</li>
<li><strong>Correlate with telemetry:</strong> compare the cost movement with utilization, request volume, throughput, and application activity.</li>
<li><strong>Record the conclusion:</strong> note whether the change was expected, unresolved, or actionable, and assign an owner.</li>
</ol>
<h2>4. Example: a sudden data-transfer increase</h2>
<p>Suppose a service's daily data-transfer cost rises from approximately 40 currency units to 95. The increase deserves attention, but the billing record alone does not explain it. Check whether a new region was enabled, an export job ran more frequently, a cache configuration changed, or traffic shifted between availability zones. Then compare transfer volume and application request metrics for the same interval.</p>
<p>If the increase matches a planned launch, it may be expected. If it coincides with an unintended cross-region data path, the team can evaluate architecture changes. In both cases, the billing anomaly is a lead—not proof of waste.</p>
<h2>5. Use Cloud Cost Linter as a screening aid</h2>
<p>Cloud Cost Linter calculates statistical outlier signals from the supplied billing rows and summarizes service spending. Its current interface labels the Z-score threshold and describes flagged values as outliers for review. It does not know your workload calendar, service-level objectives, pricing contract, or operational telemetry.</p>
<p>Try the <a href="/">analyzer</a> with sample or synthetic data. Treat every result as a candidate for human investigation. Do not automatically stop, resize, or delete a production resource based only on a billing flag.</p>
<h2>6. Measure whether detection is useful</h2>
<p>Track how many alerts were investigated, how many represented expected activity, how quickly owners responded, and whether a corrective action was verified. Tune thresholds using observed false positives and missed events. A useful system helps teams find important changes without overwhelming them with noise.</p>
<h2>Further reading</h2>
<p>Consult your cloud provider's billing and cost-management documentation for its anomaly detection features, billing export definitions, and pricing-change notices. Provider-native alerts may use additional account and usage context that a standalone CSV cannot access.</p>
"""
    },
    "duplicate-cloud-billing-charges": {
        "title": "How to Investigate Possible Duplicate Cloud Billing Charges",
        "description": "A practical checklist for validating repeated billing line items and distinguishing duplicates from legitimate charges.",
        "heading": "How to Investigate Possible Duplicate Cloud Charges",
        "body": """
<p>Two similar rows in a cloud billing export do not automatically mean that a provider charged twice for the same usage. Billing systems often split costs across time intervals, usage types, regions, accounts, discounts, taxes, and adjustments. A duplicate detector can identify records worth comparing, but only invoice and provider-side evidence can establish whether a billing error occurred.</p>
<h2>1. Understand why similar rows appear</h2>
<ul>
<li><strong>Different usage dimensions:</strong> one resource can generate separate compute, storage, request, and data-transfer charges.</li>
<li><strong>Time slicing:</strong> a provider may emit multiple line items for different usage intervals on the same date.</li>
<li><strong>Regional or account scope:</strong> similar resource names may exist in different regions, projects, or linked accounts.</li>
<li><strong>Adjustments:</strong> credits, refunds, taxes, and corrections can appear as separate positive or negative rows.</li>
<li><strong>Export revisions:</strong> rerunning or combining exports can accidentally include the same source data more than once.</li>
</ul>
<h2>2. Compare the full billing context</h2>
<p>Before treating two rows as duplicates, compare more than the amount and date. Useful fields include invoice ID, line-item ID, account or project, service, SKU, resource ID, region, usage type, quantity, unit, pricing model, billing interval, and export generation time.</p>
<p>For example, two identical-looking compute charges may represent separate virtual machines with similar names. Two rows for one resource may also represent different usage types. If the export lacks the dimensions needed to distinguish them, mark the case as unresolved rather than assuming an error.</p>
<h2>3. Follow a repeatable validation process</h2>
<ol>
<li>Preserve the original invoice and unmodified billing export.</li>
<li>Confirm that the rows belong to the same provider, account, invoice, billing period, and currency.</li>
<li>Compare unique line-item identifiers and all available usage dimensions.</li>
<li>Check whether the export was appended to an earlier file or imported more than once.</li>
<li>Review provider documentation for how credits, taxes, discounts, and adjustments are represented.</li>
<li>Reconcile the suspected rows against the provider's billing console or detailed invoice.</li>
<li>If the evidence still suggests an error, contact official billing support with invoice and line-item references.</li>
</ol>
<h2>4. Keep an evidence record</h2>
<p>For each candidate, record the invoice number, line-item identifiers, affected period, service and resource, amount and currency, comparison performed, supporting evidence, provider case number, and final outcome. Avoid placing credentials or sensitive customer data in public issue trackers or shared documents.</p>
<h2>5. Interpret automated duplicate flags carefully</h2>
<p>Cloud Cost Linter can identify rows that match its duplicate-detection criteria. This is a triage feature: it narrows the set of records that a person may want to inspect. It cannot access your provider's invoice system, determine the contractual meaning of a line item, confirm a provider mistake, or establish that a refund is due.</p>
<p>For that reason, the interface describes these as <strong>potential duplicate charges</strong> and unconfirmed candidates. Do not report flagged totals as recovered money or verified savings. A candidate becomes a confirmed billing issue only after independent provider-side validation.</p>
<h2>6. Example: repeated storage line items</h2>
<p>Imagine two rows show the same resource name, date, and amount. One row may represent provisioned storage capacity while the other represents snapshot storage or API operations. Compare SKU, usage type, quantity, unit, region, and invoice line-item ID. If those details differ, the charges may be legitimate even though the summary fields look alike.</p>
<h2>What to do next</h2>
<p>Use the <a href="/">Cloud Cost Linter hosted analyzer</a> with a synthetic or non-sensitive CSV to identify possible matches. The hosted demo transmits the selected CSV to the server for in-memory processing; do not upload confidential or sensitive billing exports. Confirm every suspected duplicate with your provider before disputing a charge or changing a financial record.</p>
"""
    },
    "cloud-rightsizing-basics": {
        "title": "Cloud Rightsizing: Metrics, Risk, and a Safe Workflow",
        "description": "A practical guide to combining billing, utilization, reliability, and workload context before rightsizing cloud resources.",
        "heading": "Cloud Rightsizing: What Billing Data Can and Cannot Prove",
        "body": """
<p>Cloud rightsizing means matching resource capacity and configuration to real workload requirements. The goal is to reduce unnecessary spend while preserving performance, reliability, security, and room for expected growth. A billing export can show where money is being spent; it usually cannot show whether a resource is oversized or safe to change.</p>
<h2>1. Start with cost, then collect utilization evidence</h2>
<p>A high charge can identify a resource worth reviewing, but cost is not a utilization metric. A virtual machine may be expensive because it runs a critical workload at low average CPU, because it has a large memory reservation, or because it is located in a costly region. Each explanation leads to a different decision.</p>
<p>Collect measurements across representative peak and off-peak periods. A short snapshot can miss batch jobs, monthly processing, seasonal traffic, or disaster-recovery activity.</p>
<h2>2. Metrics to review by resource type</h2>
<table><thead><tr><th>Resource type</th><th>Useful evidence</th><th>Important cautions</th></tr></thead><tbody>
<tr><td>Compute instances</td><td>CPU, memory, network, disk I/O, queue depth</td><td>Peak periods, throttling, burst credits, and failover capacity</td></tr>
<tr><td>Databases</td><td>CPU, memory, connections, IOPS, latency, storage growth</td><td>Replication, maintenance windows, query bursts, and recovery needs</td></tr>
<tr><td>Storage</td><td>Capacity, access frequency, retrieval rate, IOPS</td><td>Retention, retrieval fees, durability, and restore objectives</td></tr>
<tr><td>Containers</td><td>Requests, limits, throttling, restarts, pod utilization</td><td>Scheduling headroom, autoscaling behavior, and noisy neighbors</td></tr>
<tr><td>Networking</td><td>Throughput, transfer volume, route and region patterns</td><td>Latency, redundancy, and cross-region dependencies</td></tr>
</tbody></table>
<h2>3. Include reliability and business requirements</h2>
<p>Capacity decisions must account for service-level objectives, availability targets, redundancy, recovery time, recovery point, security controls, and planned growth. A resource with low average utilization may be intentionally reserved for failover or a predictable peak. Removing that headroom can increase outage risk.</p>
<h2>4. Estimate before changing</h2>
<p>Build a baseline that includes both cost and performance. Identify a candidate change, estimate its financial effect using current provider pricing, and document assumptions. Consider commitment discounts, licensing, data-transfer charges, storage performance tiers, and any migration cost. A lower instance price does not always mean a lower total bill.</p>
<h2>5. Use a safe change process</h2>
<ol>
<li>Choose a workload owner and obtain approval before changing production capacity.</li>
<li>Review telemetry over a representative business cycle.</li>
<li>Check dependencies, redundancy, capacity limits, and rollback options.</li>
<li>Test a reversible change in a non-production environment where practical.</li>
<li>Roll out gradually and monitor latency, errors, saturation, and availability.</li>
<li>Rollback promptly if service health degrades.</li>
<li>Compare subsequent invoices and performance data to verify the actual result.</li>
</ol>
<h2>6. Understand estimates and savings claims</h2>
<p>A percentage-based rightsizing estimate is a scenario, not a forecast or guarantee. The actual result depends on resource type, region, pricing model, utilization, commitments, and operational constraints. Report realized savings only after comparing like-for-like bills and confirming that service performance remains acceptable.</p>
<h2>7. What Cloud Cost Linter can contribute</h2>
<p>Cloud Cost Linter summarizes billing records, highlights statistical outliers, identifies potential duplicate rows, and displays an illustrative rightsizing estimate. It does not connect to cloud accounts or retrieve CPU, memory, storage, network, or application telemetry. Billing records alone cannot establish that a resource is idle, oversized, or safe to remove.</p>
<p>Use the <a href="/">tool</a> to identify cost records for further review, then validate candidates with provider monitoring and the workload owner. The hosted demo sends uploaded CSV content to the server for temporary in-memory processing. Do not upload confidential or sensitive billing data.</p>
<h2>Further verification</h2>
<p>Check your provider's official documentation for resource metrics, instance families, storage performance, autoscaling, pricing, and commitment discounts. Rightsizing is a controlled engineering change—not simply choosing the smallest available configuration.</p>
"""
    }
}

def _layout(title, description, heading, body, path, updated=None):
    canonical = BASE + path
    stamp = f'<p class="stamp">Last updated: {escape(updated)}</p>' if updated else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} | Cloud Cost Linter</title><meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow">
<meta property="og:type" content="article"><meta property="og:title" content="{escape(title, quote=True)} | Cloud Cost Linter">
<meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{canonical}">
<style>
:root{{--bg:#0b0f19;--panel:#111827;--line:#263244;--ink:#f3f4f6;--muted:#aab4c3;--accent:#67e8f9}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.75 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
header,footer{{border-color:var(--line);border-style:solid;padding:18px max(20px,calc((100% - 900px)/2));}}
header{{border-width:0 0 1px}}footer{{border-width:1px 0 0;color:var(--muted);font-size:14px}}
nav{{display:flex;flex-wrap:wrap;gap:18px}}a{{color:var(--accent)}}nav a{{text-decoration:none}}main{{max-width:900px;margin:42px auto;padding:0 22px 50px}}
article{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:clamp(22px,5vw,48px)}}
h1{{font-size:clamp(30px,5vw,42px);line-height:1.2;margin:0 0 12px}}h2{{font-size:22px;margin-top:30px;line-height:1.35}}
p,li{{color:#d4dbe5}}.stamp{{color:var(--muted);font-size:13px}}.back{{display:inline-block;margin-bottom:18px;text-decoration:none}}
</style></head><body>
<header><nav aria-label="Main navigation"><a href="/">Tool</a><a href="/about">About</a><a href="/guides/cloud-billing-csv-guide">Guides</a><a href="/contact">Contact</a></nav></header>
<main><a class="back" href="/">← Back to Cloud Cost Linter</a><article><h1>{escape(heading)}</h1>{stamp}{body}</article></main>
<footer>Cloud Cost Linter · Open-source cloud billing analysis tool · <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · <a href="/contact">Contact</a></footer>
</body></html>"""

def render_site_page(slug):
    page = PAGES.get(slug) or GUIDES.get(slug)
    if not page:
        return None
    path = f"/guides/{slug}" if slug in GUIDES else f"/{slug}"
    return _layout(page["title"], page["description"], page["heading"], page["body"], path, page.get("updated"))

SITE_PAGE_SLUGS = tuple(PAGES.keys())
GUIDE_SLUGS = tuple(GUIDES.keys())
