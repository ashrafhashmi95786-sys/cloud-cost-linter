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
<p>The current application code does not intentionally set advertising cookies or include third-party analytics or advertising scripts. If analytics or advertising services are added later, this policy and the site's consent practices must be updated before those services are enabled.</p>
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
<p>For questions about these terms, use the <a href="https://github.com/ashrafhashmi95786-sys/cloud-cost-linter/issues">GitHub issue tracker</a>. Do not include secrets or private billing records.</p>
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
<p>Cloud Cost Linter is an open-source project. The best way to contact the project maintainers is through GitHub, where questions and technical reports can be tracked transparently.</p>
<h2>Report a bug or request a feature</h2>
<p>Open an issue in the <a href="https://github.com/ashrafhashmi95786-sys/cloud-cost-linter/issues">Cloud Cost Linter GitHub issue tracker</a>.</p>
<h2>Contribute to the project</h2>
<p>Review the <a href="https://github.com/ashrafhashmi95786-sys/cloud-cost-linter">source repository</a> and submit a pull request with a clear description and relevant tests.</p>
<h2>Protect your information</h2>
<p>Never attach passwords, API keys, access tokens, customer details, or private billing exports to a public issue. Share only a small synthetic example that contains no confidential information.</p>
"""
    }
}

GUIDES = {
    "cloud-billing-csv-guide": {
        "title": "How to Read a Cloud Billing CSV",
        "description": "Understand the key columns in a cloud billing CSV and prepare a file for cost analysis.",
        "heading": "How to Read a Cloud Billing CSV",
        "body": """
<p>A cloud billing CSV is a record of charges reported by a cloud provider for a billing period. It is useful for cost review, but it is not a complete picture of how resources were used.</p>
<h2>Start with the important fields</h2>
<ul><li><strong>Record ID:</strong> a unique identifier for a billing line, when the provider supplies one.</li><li><strong>Service:</strong> the product or service associated with the charge.</li><li><strong>Resource ID:</strong> the resource identifier, if available.</li><li><strong>Date:</strong> the usage or billing date represented by the row.</li><li><strong>Cost:</strong> the amount charged, interpreted with the currency and billing context.</li></ul>
<h2>Check the export before analysis</h2>
<p>Confirm the billing period, currency, timezone, tax treatment, credits, discounts, and whether amounts are amortized or billed on demand. Different providers and export settings use different schemas, so map columns carefully instead of assuming that two exports are directly comparable.</p>
<h2>What a CSV cannot tell you</h2>
<p>A charge does not establish whether a resource was idle, underused, or correctly configured. Pair billing records with utilization metrics and resource inventory before recommending a change.</p>
<h2>Use Cloud Cost Linter</h2>
<p>Cloud Cost Linter expects record_id, service, resource_id, date, and cost columns. Try the <a href="/">hosted CSV analyzer</a> with a synthetic or non-sensitive example. Do not upload confidential billing exports to the public demo.</p>
"""
    },
    "cloud-billing-anomaly-detection": {
        "title": "Cloud Billing Anomaly Detection Explained",
        "description": "Learn what a cloud cost anomaly is, why statistical outliers need context, and how to investigate them.",
        "heading": "Cloud Billing Anomaly Detection Explained",
        "body": """
<p>A cloud billing anomaly is a cost pattern that differs from an expected baseline. It may indicate a configuration change, workload growth, a pricing change, a one-time operation, or a data issue.</p>
<h2>Why a statistical flag is only a starting point</h2>
<p>Methods such as standard deviation and Z-scores compare observations with a statistical baseline. A high score can identify a value worth reviewing, but the score does not explain the business or technical cause. Small datasets, seasonal workloads, and highly variable services can produce misleading signals.</p>
<h2>A practical investigation sequence</h2>
<ol><li>Confirm the billing period, currency, and export completeness.</li><li>Compare the charge with the same service and resource over prior periods.</li><li>Check deployments, scaling events, data transfer, storage growth, and pricing changes.</li><li>Correlate the charge with provider metrics and application activity.</li><li>Document the cause and the action taken.</li></ol>
<h2>Keep human review in the loop</h2>
<p>Do not automatically stop or resize a resource based only on a billing anomaly. Verify operational impact and obtain the appropriate owner approval first.</p>
<p><a href="/">Analyze a sample billing CSV with Cloud Cost Linter</a>.</p>
"""
    },
    "duplicate-cloud-billing-charges": {
        "title": "How to Investigate Possible Duplicate Cloud Charges",
        "description": "A careful process for checking repeated cloud billing records without mistaking legitimate charges for duplicates.",
        "heading": "How to Investigate Possible Duplicate Cloud Charges",
        "body": """
<p>Repeated-looking billing rows are not automatically duplicate charges. Cloud providers may create separate line items for usage intervals, regions, projects, taxes, credits, adjustments, or different billing dimensions.</p>
<h2>Compare more than the amount</h2>
<p>Review the record identifiers, service, resource, usage dates, region, SKU, project or account, quantity, unit, and billing export version. Similar amounts on the same date can still represent distinct usage.</p>
<h2>Validate with the provider</h2>
<p>Check the detailed invoice and provider billing documentation. If the records still appear duplicated, contact the provider through its official billing support process and retain the invoice and relevant line-item references.</p>
<h2>Interpret automated flags carefully</h2>
<p>A duplicate-detection tool can identify candidate rows for review. It cannot confirm that the provider made an error or that a refund is due. Treat flagged values as investigation candidates, not realized savings.</p>
"""
    },
    "cloud-rightsizing-basics": {
        "title": "Cloud Rightsizing: What Billing Data Can and Cannot Prove",
        "description": "Understand how to combine cloud billing data and utilization metrics before rightsizing resources.",
        "heading": "Cloud Rightsizing: What Billing Data Can and Cannot Prove",
        "body": """
<p>Cloud rightsizing means matching a resource's capacity and configuration to its actual workload requirements. The goal is to reduce unnecessary cost without harming reliability, performance, or future capacity needs.</p>
<h2>Billing data shows cost, not utilization</h2>
<p>A high monthly charge may justify investigation, but billing exports usually do not show CPU, memory, disk I/O, network throughput, latency, or service-level objectives. A low charge does not prove that a resource is safe to remove either.</p>
<h2>Metrics to review</h2>
<ul><li>CPU and memory utilization across representative peak periods.</li><li>Storage capacity, IOPS, throughput, and growth.</li><li>Network traffic and data-transfer patterns.</li><li>Latency, error rates, queue depth, and workload seasonality.</li><li>Availability, redundancy, and recovery requirements.</li></ul>
<h2>Make changes safely</h2>
<p>Build a baseline, identify a reversible change, test it, monitor service health, and keep a rollback plan. Get approval from the workload owner before changing production capacity.</p>
<h2>Interpret estimates honestly</h2>
<p>A percentage-based savings estimate is a scenario, not a guarantee. Confirm actual savings against subsequent invoices and operational metrics.</p>
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
