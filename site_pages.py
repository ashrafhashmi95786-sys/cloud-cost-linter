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
<p>You can use the local version of the open-source tool to process files on your own computer. For questions or privacy-related requests, email <a href="mailto:ashwebtools95@gmail.com">ashwebtools95@gmail.com</a>. Do not email passwords, API keys, access tokens, customer details, or confidential billing exports.</p>
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
<h2>What to include in a support request</h2>
<p>To help us understand a problem, include the page or feature you were using, the steps that led to the issue, the result you expected, and the result you actually saw. If an error message appears, copy its text without including private data.</p>
<h2>Response expectations</h2>
<p>Cloud Cost Linter is maintained as an open-source project. Support is provided on a best-effort basis, so a response time is not guaranteed. For code defects or reproducible feature requests, the GitHub issue tracker is the preferred place to share details and follow progress.</p>
<h2>Responsible disclosure</h2>
<p>If you believe you have found a security vulnerability, please do not publish exploit details or sensitive information in a public issue. Contact the project by email with a concise description and safe reproduction steps so the concern can be reviewed responsibly.</p>
"""
    }
}

GUIDES = {
    "cloud-billing-csv-guide": {
        "title": "Read a Cloud Billing CSV: Practical Guide",
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
<h2>Official provider documentation</h2>
<p>For provider-specific field definitions, billing behavior, pricing, and recommendations, consult the current official documentation:</p>
<ul>
<li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/" rel="noopener noreferrer">AWS Billing and Cost Management</a></li>
<li><a href="https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-improved-exports" rel="noopener noreferrer">Azure Cost Management exports</a></li>
<li><a href="https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery" rel="noopener noreferrer">Google Cloud Billing export to BigQuery</a></li>
</ul>
"""
    },
    "cloud-billing-anomaly-detection": {
        "title": "Cloud Billing Anomaly Detection Methods",
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
<h2>Official provider documentation</h2>
<p>For provider-specific field definitions, billing behavior, pricing, and recommendations, consult the current official documentation:</p>
<ul>
<li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/view-billing-dashboard.html" rel="noopener noreferrer">AWS billing dashboard and cost anomaly monitoring</a></li>
<li><a href="https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/overview-cost-management" rel="noopener noreferrer">Microsoft Cost Management overview</a></li>
<li><a href="https://docs.cloud.google.com/billing/docs/how-to/manage-anomalies" rel="noopener noreferrer">Google Cloud cost anomalies</a></li>
</ul>
"""
    },
    "duplicate-cloud-billing-charges": {
        "title": "Investigate Duplicate Cloud Billing Charges",
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
<h2>Official provider documentation</h2>
<p>For provider-specific field definitions, billing behavior, pricing, and recommendations, consult the current official documentation:</p>
<ul>
<li><a href="https://docs.aws.amazon.com/us_en/awsaccountbilling/latest/aboutv2/differences-billing-data-cost-explorer-data.html" rel="noopener noreferrer">AWS: differences between billing and Cost Explorer data</a></li>
<li><a href="https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/understand-cost-mgt-data" rel="noopener noreferrer">Azure: understand cost management data</a></li>
<li><a href="https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery" rel="noopener noreferrer">Google Cloud Billing export and detailed cost records</a></li>
</ul>
"""
    },
    "cloud-rightsizing-basics": {
        "title": "Cloud Rightsizing: Metrics and Safe Steps",
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
<h2>Official provider documentation</h2>
<p>For provider-specific field definitions, billing behavior, pricing, and recommendations, consult the current official documentation:</p>
<ul>
<li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html" rel="noopener noreferrer">AWS cost optimization and rightsizing resources</a></li>
<li><a href="https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/overview-cost-management" rel="noopener noreferrer">Microsoft Cost Management and Azure cost recommendations</a></li>
</ul>
"""
    }
    ,
    "cloud-cost-allocation-tagging": {
        "title": "Cloud Cost Allocation and Tagging Guide",
        "description": "A practical framework for allocating cloud spend with account structure, tags, shared-cost rules, and coverage checks.",
        "heading": "Cloud Cost Allocation and Tagging",
        "body": """
<p>Cloud cost allocation connects infrastructure spending to the teams, products, environments, and business activities that create or benefit from it. A useful allocation model helps people understand costs and take responsibility for them. It is not simply a matter of adding tags: the model must define ownership, handle shared services, and make missing information visible.</p>
<h2>1. Decide what you want to allocate</h2>
<p>Start with the decisions the data should support. Engineering teams may need resource-level costs, product leaders may need product totals, and finance may need monthly cost by business unit. Choose a small set of dimensions that answer real questions, such as owner, application, environment, cost centre, and business unit. Avoid creating dozens of mandatory tags before agreeing how they will be used.</p>
<h2>2. Establish a consistent taxonomy</h2>
<p>Write down the allowed values and their meaning. For example, environment values might be production, staging, development, and sandbox. Define whether names are case-sensitive, how legacy values are handled, and who can approve a new value. Prefer stable identifiers for teams and products over display names that change during reorganizations.</p>
<p>Apply the same definitions across accounts, projects, subscriptions, and infrastructure-as-code templates. Where a provider supports inherited labels or account-level metadata, use them to reduce manual tagging. Keep a documented mapping for resources that cannot carry tags.</p>
<h2>3. Measure coverage, not just tagged spend</h2>
<p>A report showing that most spend has an owner can still hide a large unallocated service. Track coverage by both resource count and cost. Separate missing tags, invalid values, conflicting owners, and resources that cannot be tagged. Assign an owner and remediation date to each important gap.</p>
<table><thead><tr><th>Coverage measure</th><th>What it reveals</th><th>Useful follow-up</th></tr></thead><tbody>
<tr><td>Spend with a valid owner</td><td>How much cost can be assigned to a responsible team</td><td>Investigate high-cost unowned resources</td></tr>
<tr><td>Resources with required tags</td><td>Whether tagging is consistently applied</td><td>Fix templates and provisioning workflows</td></tr>
<tr><td>Invalid or conflicting values</td><td>Whether the taxonomy is being followed</td><td>Publish allowed values and validation rules</td></tr>
<tr><td>Unallocated shared spend</td><td>How much central cost still needs a policy</td><td>Review shared-cost allocation methods</td></tr>
</tbody></table>
<h2>4. Choose a transparent shared-cost method</h2>
<p>Networking, security, observability, support, and platform services often benefit many teams. Possible methods include leaving costs in a central shared-services bucket, allocating by measured usage, or distributing by an agreed proxy such as active users or compute consumption. The right method depends on the service and the quality of available measurements.</p>
<p>Document the method, data source, frequency, and limitations. Do not present an estimated allocation as a direct provider charge. Keep both the original bill and any internal allocation view so finance can reconcile the two.</p>
<h2>5. Reconcile the model each billing cycle</h2>
<ol>
<li>Confirm the billing export covers the full period and expected accounts.</li>
<li>Normalize account, project, team, and environment identifiers.</li>
<li>Calculate tagged, untagged, invalid, and shared spend separately.</li>
<li>Compare allocated totals with the provider invoice and explain any differences.</li>
<li>Review ownership changes and retire obsolete tag values.</li>
<li>Publish exceptions with an owner and a target date.</li>
</ol>
<h2>6. Avoid common allocation mistakes</h2>
<ul>
<li>Using free-form team names that differ across accounts.</li>
<li>Assuming every provider charge maps cleanly to one resource tag.</li>
<li>Allocating shared costs without explaining the chosen proxy.</li>
<li>Ignoring credits, taxes, discounts, and marketplace charges.</li>
<li>Changing historical allocation rules without preserving the old method.</li>
</ul>
<h2>How Cloud Cost Linter fits in</h2>
<p>Cloud Cost Linter can summarize the supported billing rows and help identify cost records for follow-up, but its current input schema does not provide a full allocation engine or validate an organization's tag taxonomy. Preserve provider dimensions in your source export and use your billing platform or a dedicated FinOps data model for detailed ownership reporting. Try the <a href="/">hosted analyzer</a> only with synthetic or non-sensitive data; uploaded CSV content is transmitted to the server for in-memory processing.</p>
<h2>Further verification</h2>
<p>Check your cloud provider's current documentation for cost-allocation tags, inherited labels, billing exports, and account-level metadata. Provider behavior differs, and some tags must be activated for billing reports before they appear in exports.</p>
<h2>Official provider documentation</h2>
<p>For provider-specific field definitions, billing behavior, pricing, and recommendations, consult the current official documentation:</p>
<ul>
<li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html" rel="noopener noreferrer">AWS cost allocation tags</a></li>
<li><a href="https://learn.microsoft.com/azure/cost-management-billing/costs/allocate-costs" rel="noopener noreferrer">Azure cost allocation</a></li>
<li><a href="https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery" rel="noopener noreferrer">Google Cloud Billing export fields, including labels</a></li>
</ul>
"""
    },
    "cloud-budget-forecast-variance": {
        "title": "Cloud Budgets and Forecast Variance Guide",
        "description": "Learn to set useful cloud budgets, interpret forecasts, investigate variance, and avoid alert fatigue.",
        "heading": "Cloud Budgets, Forecasts, and Variance",
        "body": """
<p>A cloud budget is a spending limit or planning reference for a defined scope and period. A forecast estimates where spending may land if current patterns continue. Variance is the difference between actual or forecast spend and the budget or baseline. Used together, these tools help teams act before a cost surprise becomes a month-end problem.</p>
<h2>1. Define the budget scope</h2>
<p>Specify the owner, account or project, services included, currency, time period, and whether the budget is gross or net of credits and discounts. Align the scope with the decision-maker who can investigate or change the workload. A company-wide budget may be useful for leadership, while team-level budgets make operational ownership clearer.</p>
<p>Keep one-time migration work, experiments, and recurring production spend distinguishable where possible. If a budget includes taxes, support, marketplace products, or committed-use fees, state that explicitly so comparisons remain consistent.</p>
<h2>2. Build a baseline before setting a target</h2>
<p>Use several comparable billing periods and annotate known changes such as launches, seasonal demand, migrations, pricing changes, and commitment purchases. A simple average can be misleading when usage is seasonal or a product is growing quickly. For a new workload, estimate from expected usage and current provider pricing, then revisit the assumptions after real data arrives.</p>
<h2>3. Understand what a forecast can and cannot say</h2>
<p>A straight-line forecast projects recent spending forward. It is easy to explain but can overstate a temporary spike or understate a workload that is ramping up. More advanced forecasts may account for seasonality, planned events, usage drivers, and known price changes. Every forecast should state its data window, assumptions, and uncertainty.</p>
<p>Do not treat a forecast as an invoice. Delayed usage records, credits, refunds, taxes, currency conversion, and provider adjustments can change the final bill. Compare forecasts with the same cost basis and billing scope each time.</p>
<h2>4. Set alerts that lead to action</h2>
<p>Useful alerts identify who should act and what they should check. Consider an early warning at a lower percentage of budget, a stronger warning near the expected limit, and an escalation when the forecast exceeds the approved amount. Tune thresholds to the size and volatility of the workload rather than copying one percentage across every team.</p>
<table><thead><tr><th>Signal</th><th>Question to ask</th><th>Possible response</th></tr></thead><tbody>
<tr><td>Actual spend rises faster than expected</td><td>Did usage, deployment volume, or pricing change?</td><td>Compare usage drivers and recent releases</td></tr>
<tr><td>Forecast exceeds budget</td><td>Is the increase planned and funded?</td><td>Update the plan or investigate the variance</td></tr>
<tr><td>Spend is unusually low</td><td>Is the export incomplete or did a workload stop?</td><td>Check service health and billing coverage</td></tr>
<tr><td>Repeated alerts have no action</td><td>Is the scope or threshold useful?</td><td>Change ownership, routing, or threshold</td></tr>
</tbody></table>
<h2>5. Investigate variance systematically</h2>
<ol>
<li>Confirm the billing period, currency, account scope, and export completeness.</li>
<li>Separate usage changes from price, discount, tax, and credit changes.</li>
<li>Break down the variance by service, region, project, SKU, and resource where available.</li>
<li>Compare the timing with deployments, traffic, batch jobs, and business events.</li>
<li>Record the cause, owner, action, and whether the budget or forecast needs updating.</li>
</ol>
<h2>6. Make budget reviews operational</h2>
<p>Hold a regular review with engineering, finance, and product owners. Focus on the largest material variances, upcoming launches, forecast confidence, and actions that have an accountable owner. Track whether previous actions changed spend and workload outcomes. A budget review should improve decisions, not become a meeting that merely reads a dashboard.</p>
<h2>7. Avoid misleading comparisons</h2>
<ul>
<li>Do not compare a partial month with a complete month without normalizing the period.</li>
<li>Do not mix amortized and cash-based commitment costs without labelling them.</li>
<li>Do not interpret a credit or refund as a sustainable reduction in usage cost.</li>
<li>Do not cut reliability or security controls solely to meet a budget threshold.</li>
</ul>
<h2>How Cloud Cost Linter fits in</h2>
<p>Cloud Cost Linter analyzes a supplied CSV and highlights spending summaries and unusual records. It does not maintain budgets, forecast future bills, or connect to provider billing APIs. Use its output as an investigation input alongside your provider's native budgets, cost explorer, and forecast tools. For the hosted demo, use synthetic or non-sensitive files only; uploaded CSV content is sent to the server for in-memory processing.</p>
<h2>Official provider documentation</h2>
<p>For provider-specific field definitions, billing behavior, pricing, and recommendations, consult the current official documentation:</p>
<ul>
<li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/view-billing-dashboard.html" rel="noopener noreferrer">AWS budgets and cost monitoring</a></li>
<li><a href="https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/overview-cost-management" rel="noopener noreferrer">Microsoft Cost Management budgets and alerts</a></li>
<li><a href="https://docs.cloud.google.com/billing/docs/how-to/budgets" rel="noopener noreferrer">Google Cloud budgets and budget alerts</a></li>
</ul>
"""
    },
    "cloud-data-transfer-costs": {
        "title": "Cloud Data Transfer Costs Guide",
        "description": "Understand common cloud data-transfer charges, trace network cost drivers, and evaluate optimizations without harming reliability.",
        "heading": "Cloud Data Transfer Costs",
        "body": """
<p>Cloud data-transfer charges can be difficult to interpret because a bill may separate internet egress, inter-region transfer, cross-zone traffic, content delivery, load balancing, and managed network services. The same application request can generate several billable network events. A useful investigation starts by identifying the exact meter and traffic path rather than assuming all network spend is one category.</p>
<h2>1. Identify the charge type</h2>
<p>Read the provider's usage type, SKU, region, source and destination dimensions, quantity, and unit. Determine whether the line represents data leaving a provider, traffic between regions or zones, a private connectivity service, a gateway, or a content delivery service. Names and pricing rules vary by provider and product.</p>
<p>Check whether the charge is measured in decimal gigabytes or binary gibibytes, whether it is rounded, and whether the export reports gross usage or usage after a free allowance. These details matter when reconciling usage with application metrics.</p>
<h2>2. Trace the traffic path</h2>
<p>Map the main request and data paths: users to edge, edge to origin, service to database, service to object storage, and traffic between regions or zones. Look for repeated transfers caused by chatty service calls, cross-region reads, duplicated replication, backup copies, or workloads placed far from their data.</p>
<p>Correlate billing dimensions with flow logs, load-balancer metrics, CDN reports, storage access logs, and application telemetry. Billing records can identify the cost category but usually cannot reveal which application request caused it.</p>
<h2>3. Evaluate common optimization options</h2>
<table><thead><tr><th>Potential change</th><th>When it may help</th><th>What to verify</th></tr></thead><tbody>
<tr><td>Use a CDN or cache</td><td>Repeated delivery of cacheable content</td><td>Cache hit rate, invalidation, origin load, and edge pricing</td></tr>
<tr><td>Co-locate compute and data</td><td>Frequent transfers across regions or zones</td><td>Availability, latency, disaster recovery, and resilience</td></tr>
<tr><td>Reduce chatty service calls</td><td>Many small repeated network requests</td><td>Payload size, batching latency, and failure behavior</td></tr>
<tr><td>Compress or transform payloads</td><td>Large compressible responses or objects</td><td>CPU overhead, compatibility, and end-to-end latency</td></tr>
<tr><td>Review replication and backups</td><td>Unnecessary duplicate copies or excessive frequency</td><td>Retention, recovery objectives, and compliance</td></tr>
</tbody></table>
<h2>4. Model total cost, not just egress price</h2>
<p>A change that reduces one transfer meter may increase another cost. A CDN can add request and cache-fill charges. Moving a database closer to an application may change compute pricing or resilience. Compression can increase CPU use. Reducing replication can affect recovery objectives. Estimate the complete design cost and operational trade-offs before making a change.</p>
<h2>5. Use a safe investigation workflow</h2>
<ol>
<li>Choose a billing period and reconcile network charges with the provider invoice.</li>
<li>Group usage by meter, region, source, destination, and service where the export supports it.</li>
<li>Compare usage volume with flow logs, CDN reports, and application traffic metrics.</li>
<li>Identify a specific traffic path and propose one reversible change.</li>
<li>Estimate all affected charges and review reliability, latency, security, and recovery requirements.</li>
<li>Test with a representative workload and monitor both performance and cost.</li>
<li>Compare subsequent bills using the same units, scope, and pricing basis.</li>
</ol>
<h2>6. Common pitfalls</h2>
<ul>
<li>Assuming all outbound data is charged at one universal rate.</li>
<li>Ignoring inter-region, inter-zone, gateway, or CDN request charges.</li>
<li>Comparing traffic volumes measured in different units.</li>
<li>Disabling replication or redundancy without reviewing recovery needs.</li>
<li>Claiming savings from a traffic reduction before the bill confirms it.</li>
</ul>
<h2>How Cloud Cost Linter fits in</h2>
<p>Cloud Cost Linter can summarize cost rows and flag unusual records when the export includes network services. It does not inspect packet flows, identify application endpoints, or calculate provider-specific network prices. Preserve usage type, region, and SKU fields in the source data and use provider network telemetry for root-cause analysis. Use synthetic or non-sensitive files with the hosted demo because uploaded CSV content is transmitted to the server for in-memory processing.</p>
<h2>Further verification</h2>
<p>Consult the current network pricing pages and data-transfer documentation for your provider, region, service, and pricing agreement. Network rates and free allowances can differ substantially across products and locations.</p>
<h2>Official provider documentation</h2>
<p>For provider-specific field definitions, billing behavior, pricing, and recommendations, consult the current official documentation:</p>
<ul>
<li><a href="https://cloud.google.com/vpc/network-pricing" rel="noopener noreferrer">Google Cloud network pricing</a></li>
<li><a href="https://azure.microsoft.com/en-us/pricing/details/bandwidth/" rel="noopener noreferrer">Azure bandwidth pricing</a></li>
<li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/" rel="noopener noreferrer">AWS Billing and Cost Management documentation</a></li>
</ul>
"""
    },
    "cloud-commitment-discounts": {
        "title": "Cloud Commitment Discounts Guide",
        "description": "Compare cloud commitment discounts with on-demand usage, evaluate utilization risk, and build a careful purchase decision.",
        "heading": "Cloud Commitment Discounts and Break-Even Analysis",
        "body": """
<p>Cloud providers offer commitment-based discounts in exchange for agreeing to a level of spend, usage, or capacity over a defined term. Depending on the product, these may be called reservations, savings plans, committed-use discounts, or capacity reservations. They can reduce eligible costs, but they also introduce utilization, flexibility, and financial risks.</p>
<h2>1. Distinguish a price discount from capacity assurance</h2>
<p>A pricing commitment may lower the rate applied to eligible usage without guaranteeing that capacity will be available. A capacity reservation may help secure resources in a particular location or configuration, but it may not provide the same discount as a separate pricing commitment. Read the exact product terms before comparing offers.</p>
<h2>2. Understand the commitment dimensions</h2>
<p>Check the commitment amount, term, payment option, eligible services, regions, instance families, usage flexibility, sharing rules, and cancellation or modification limits. Some commitments are measured per hour, some by total spend, and others by specific capacity attributes. A discount only applies when actual usage matches the eligible scope under the provider's rules.</p>
<h2>3. Estimate a realistic eligible baseline</h2>
<p>Use historical usage over a representative period and separate stable production workloads from experiments, seasonal workloads, migrations, and services likely to change. Exclude temporary spikes unless they are expected to continue. Model growth and contraction scenarios rather than assuming that last month's usage will repeat.</p>
<p>Check whether the historical cost view is based on on-demand rates, amortized commitment costs, or net effective rates. Mixing these views can make an offer appear more attractive than it is.</p>
<h2>4. Calculate break-even and utilization risk</h2>
<p>Compare the cost of eligible usage at on-demand rates with the commitment's total cost over the same period. Include upfront payments, recurring fees, expected eligible usage, and any residual on-demand usage. A simplified utilization measure is the portion of committed value or capacity actually consumed by eligible workloads, but the provider's own billing definition should be used for the final calculation.</p>
<table><thead><tr><th>Scenario</th><th>What to model</th><th>Decision risk</th></tr></thead><tbody>
<tr><td>Stable baseline</td><td>Expected eligible usage remains near the observed level</td><td>Check that workload and product scope remain stable</td></tr>
<tr><td>Usage declines</td><td>Eligible demand falls during the term</td><td>Unused commitment may erase expected savings</td></tr>
<tr><td>Usage grows</td><td>Demand exceeds the committed amount</td><td>Incremental usage may still be billed at on-demand rates</td></tr>
<tr><td>Architecture changes</td><td>Workload moves region, family, or service</td><td>Existing commitment may not match the new footprint</td></tr>
</tbody></table>
<h2>5. Compare flexibility and operational risk</h2>
<p>A larger discount is not automatically the best choice. A flexible commitment may have a lower discount but fit changing workloads better. Review term length, exchange or modification rules, sharing across accounts, regional restrictions, and what happens when a service is retired. Consider the organization's cash-flow policy and approval process for long-term commitments.</p>
<h2>6. A practical decision checklist</h2>
<ol>
<li>Confirm the exact product, eligibility rules, term, payment option, and cancellation terms.</li>
<li>Build an eligible usage baseline from reconciled billing and workload forecasts.</li>
<li>Model conservative, expected, and growth scenarios.</li>
<li>Calculate total commitment cost and residual on-demand spend for each scenario.</li>
<li>Check flexibility across accounts, regions, services, and resource families.</li>
<li>Obtain finance and workload-owner approval before purchasing.</li>
<li>Track utilization, coverage, effective discount, and unused commitment regularly.</li>
</ol>
<h2>7. Monitor after purchase</h2>
<p>Review commitment utilization and coverage separately. High utilization can indicate that the commitment is being consumed; coverage shows how much eligible usage benefits from a commitment. A commitment can be fully utilized while a substantial amount of other eligible usage remains on demand. Investigate low utilization early and use only the adjustment options permitted by the provider's contract.</p>
<h2>How Cloud Cost Linter fits in</h2>
<p>Cloud Cost Linter can summarize supported cost rows and identify unusual records, but it does not calculate commitment eligibility, optimize reservations, or model provider-specific discount terms. Use the provider's commitment recommendations and detailed billing exports for the decision. Do not treat an anomaly or rightsizing estimate as evidence that a commitment should be purchased. Use synthetic or non-sensitive CSV files with the hosted demo because uploaded content is transmitted to the server for in-memory processing.</p>
<h2>Further verification</h2>
<p>Review the current commitment documentation and pricing calculator for the exact provider, service, region, and payment option. Commitment products and exchange rules change, so verify current terms before making a financial commitment.</p>
<h2>Official provider documentation</h2>
<p>For provider-specific field definitions, billing behavior, pricing, and recommendations, consult the current official documentation:</p>
<ul>
<li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html" rel="noopener noreferrer">AWS Savings Plans and commitment management</a></li>
<li><a href="https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-improved-exports" rel="noopener noreferrer">Azure exports: actual and amortized cost data</a></li>
<li><a href="https://docs.cloud.google.com/billing/docs/how-to/export-data-bigquery" rel="noopener noreferrer">Google Cloud committed use discount billing export</a></li>
</ul>
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
header{{border-width:0 0 1px}}footer{{border-width:1px 0 0;color:#cbd5e1;font-size:14px}}
footer a{{color:#67e8f9;font-weight:600;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}}footer a:hover,footer a:focus-visible{{color:#a5f3fc}}footer a:focus-visible{{outline:2px solid #67e8f9;outline-offset:3px;border-radius:2px}}
nav{{display:flex;flex-wrap:wrap;gap:18px}}a{{color:var(--accent)}}nav a{{text-decoration:none}}main{{max-width:900px;margin:42px auto;padding:0 22px 50px}}
article{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:clamp(22px,5vw,48px)}}
h1{{font-size:clamp(30px,5vw,42px);line-height:1.2;margin:0 0 12px}}h2{{font-size:22px;margin-top:30px;line-height:1.35}}
p,li{{color:#d4dbe5}}.stamp{{color:var(--muted);font-size:13px}}.back{{display:inline-block;margin-bottom:18px;text-decoration:none}}
</style></head><body>
<header><nav aria-label="Main navigation"><a href="/">Tool</a><a href="/about">About</a><a href="/guides">Guides</a><a href="/contact">Contact</a></nav></header>
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


def render_guides_index():
    """Render a browsable index of all original FinOps guides."""
    cards = []
    for slug, guide in GUIDES.items():
        cards.append(
            '<article class="guide-card">'
            f'<h2><a href="/guides/{escape(slug, quote=True)}">{escape(guide["heading"])}</a></h2>'
            f'<p>{escape(guide["description"])}</p>'
            f'<a class="read-link" href="/guides/{escape(slug, quote=True)}">Read guide <span aria-hidden="true">→</span></a>'
            '</article>'
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cloud FinOps Guides and Tutorials | Cloud Cost Linter</title>
<meta name="description" content="Browse practical cloud FinOps guides covering billing CSVs, anomaly detection, duplicate charges, rightsizing, cost allocation, forecasting, data transfer, and commitment discounts.">
<link rel="canonical" href="{BASE}/guides"><meta name="robots" content="index,follow">
<meta property="og:type" content="website"><meta property="og:title" content="Cloud FinOps Guides | Cloud Cost Linter">
<meta property="og:description" content="Practical tutorials for understanding cloud bills and investigating cloud costs."><meta property="og:url" content="{BASE}/guides">
<style>
:root{{--bg:#0b0f19;--panel:#111827;--line:#263244;--ink:#f3f4f6;--muted:#aab4c3;--accent:#67e8f9}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
header,footer{{border-color:var(--line);border-style:solid;padding:18px max(20px,calc((100% - 1000px)/2))}}
header{{border-width:0 0 1px}}footer{{border-width:1px 0 0;color:#cbd5e1;font-size:14px}}
nav{{display:flex;flex-wrap:wrap;gap:18px}}a{{color:var(--accent)}}nav a{{text-decoration:none}}
main{{max-width:1000px;margin:42px auto;padding:0 22px 54px}}
h1{{font-size:clamp(30px,5vw,42px);line-height:1.2;margin:0 0 12px}}
.intro{{color:#d4dbe5;max-width:760px;margin:0 0 28px}}
.guide-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}}
.guide-card{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px;display:flex;flex-direction:column;min-height:190px}}
.guide-card h2{{font-size:20px;line-height:1.35;margin:0 0 10px}}.guide-card h2 a{{text-decoration:none}}
.guide-card p{{color:#cbd5e1;margin:0 0 18px}}.read-link{{font-weight:650;text-decoration:underline;text-underline-offset:3px;margin-top:auto}}
.back{{display:inline-block;margin-bottom:18px;text-decoration:none}}
footer a{{color:#67e8f9;font-weight:600;text-decoration:underline;text-underline-offset:3px}}
footer a:focus-visible,nav a:focus-visible,.guide-card a:focus-visible{{outline:2px solid #67e8f9;outline-offset:4px;border-radius:3px}}
@media(max-width:640px){{main{{margin:26px auto;padding:0 16px 40px}}.guide-grid{{grid-template-columns:1fr}}.guide-card{{min-height:0;padding:20px}}}}
</style></head><body>
<header><nav aria-label="Main navigation"><a href="/">Tool</a><a href="/about">About</a><a href="/guides" aria-current="page">Guides</a><a href="/contact">Contact</a></nav></header>
<main><a class="back" href="/">← Back to Cloud Cost Linter</a>
<h1>Cloud FinOps Guides</h1>
<p class="intro">Practical, independent guides to help you understand cloud billing data, investigate unusual costs, and make better-informed FinOps decisions. Each guide explains what to check, common pitfalls, and where Cloud Cost Linter can help.</p>
<section class="guide-grid" aria-label="All cloud FinOps guides">{''.join(cards)}</section>
</main>
<footer>Cloud Cost Linter · Open-source cloud billing analysis tool · <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · <a href="/contact">Contact</a></footer>
</body></html>"""
