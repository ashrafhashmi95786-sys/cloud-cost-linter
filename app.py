"""Render-compatible WSGI web application for Cloud Cost Linter.

Uploaded CSV content is processed in memory by this service and is not intentionally
written to disk. Because this is a hosted service, CSV content is transmitted to the
hosting provider; users should not upload confidential billing exports.
"""
import json
import os
from flask import Flask, Response, jsonify, request
from werkzeug.exceptions import RequestEntityTooLarge

from cloud_cost_linter import CloudCostLinter, CloudCostLinterError
from cloud_cost_linter_web import INDEX_HTML, MAX_UPLOAD_SIZE, _safe_download_stem
from site_pages import GUIDE_SLUGS, SITE_PAGE_SLUGS, render_guides_index, render_site_page

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_SIZE + (64 * 1024)

# Avoid implying browser-only/local processing on the hosted deployment.
HOSTED_HTML = (
    INDEX_HTML
    .replace("<title>Cloud Cost Linter — Local Privacy-First Billing Analyzer</title>",
             "<title>Cloud Cost Linter — Cloud Billing Analyzer</title>")
    .replace("● 100% Local · Zero Telemetry", "● Free Online Tool · In-Memory Processing")
    .replace("Analyze your monthly cloud spending CSV without sharing data or using command lines. Your files never leave your computer.",
             "Analyze a cloud billing CSV in your browser. For this hosted demo, the CSV is sent to the server for temporary in-memory processing; do not upload confidential or sensitive billing data.")
    .replace("Strict local parsing · Max 10MB", "Server-side processing · Max 10MB")
    .replace("Autonomous AI Society · Mission 002 Product Upgrade · Zero-Budget FinOps Engineering · 100% Offline & Private",
             "Cloud Cost Linter · Hosted demo. Uploaded CSV content is processed in memory and is not intentionally saved by the application.")
)
HOSTED_HTML = HOSTED_HTML.replace(
    '<title>Cloud Cost Linter — Cloud Billing Audit</title>',
    '<title>Cloud Cost Linter — Free Cloud Billing CSV Analyzer</title>'
).replace(
    '</head>',
    '<link rel="canonical" href="https://cloud-cost-linter.onrender.com/"><meta name="robots" content="index,follow"></head>'
)
HOSTED_HTML = HOSTED_HTML.replace(
    'Autonomous AI Society · Mission 002 Product Upgrade · In-Memory CSV Analysis · No Intentional CSV Persistence',
    'Cloud Cost Linter · Open-source cloud billing analysis · <a href="/about">About</a> · <a href="/guides">Guides</a> · <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a> · <a href="/contact">Contact</a>'
)
HOSTED_HTML = HOSTED_HTML.replace(
    '<!-- Upload Zone -->',
    '<div class="disclaimer-banner"><strong>Hosted demo privacy notice:</strong> Your selected CSV is transmitted to this server for analysis. The application processes it in memory and does not intentionally save the uploaded CSV. Hosting infrastructure may process request metadata. Do not upload confidential, customer-identifying, or sensitive billing data.</div>\n    <!-- Upload Zone -->'
)

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'"
    )
    if request.path == "/social-preview.svg":
        response.headers["Cache-Control"] = "public, max-age=86400"
    else:
        response.headers["Cache-Control"] = "no-store"
    return response

@app.errorhandler(RequestEntityTooLarge)
def too_large(_error):
    return jsonify(error="Request exceeds the 10 MB upload limit."), 413

@app.get("/")
@app.get("/index.html")
def index():
    return Response(HOSTED_HTML, mimetype="text/html")

@app.get("/robots.txt")
def robots_txt():
    body = "User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: https://cloud-cost-linter.onrender.com/sitemap.xml\n"
    return Response(body, mimetype="text/plain")

@app.get("/sitemap.xml")
def sitemap():
    paths = ["/"] + ["/" + slug for slug in SITE_PAGE_SLUGS] + ["/guides"] + ["/guides/" + slug for slug in GUIDE_SLUGS]
    urls = "".join("<url><loc>https://cloud-cost-linter.onrender.com" + path + "</loc></url>" for path in paths)
    xml = '<?xml version="1.0" encoding="UTF-8"?>' + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>"
    return Response(xml, mimetype="application/xml")

@app.get("/google2e731cb1546f4a5a.html")
def google_search_console_verification():
    return Response(
        "google-site-verification: google2e731cb1546f4a5a.html",
        mimetype="text/html",
    )


@app.get("/<slug>")
def public_page(slug):
    if slug not in SITE_PAGE_SLUGS:
        return Response("Page not found.", status=404, mimetype="text/plain")
    return Response(render_site_page(slug), mimetype="text/html")

@app.get("/guides")
def guides_index():
    return Response(render_guides_index(), mimetype="text/html")

@app.get("/guides/<slug>")
def guide_page(slug):
    if slug not in GUIDE_SLUGS:
        return Response("Page not found.", status=404, mimetype="text/plain")
    return Response(render_site_page(slug), mimetype="text/html")

@app.get("/social-preview.svg")
def social_preview():
    path = os.path.join(os.path.dirname(__file__), "social-preview.svg")
    try:
        with open(path, "rb") as handle:
            return Response(handle.read(), mimetype="image/svg+xml")
    except OSError:
        return Response("Social preview image not found.", status=404, mimetype="text/plain")

@app.get("/api/health")
def health():
    return jsonify(status="ok", application="Cloud Cost Linter", version="2.1.0",
                   privacy="Hosted demo: CSV content is transmitted to this server for in-memory processing.")

@app.get("/api/sample")
def sample():
    path = os.path.join(os.path.dirname(__file__), "sample_billing.csv")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return Response(handle.read(), mimetype="text/csv")
    except OSError:
        return jsonify(error="Sample billing file is unavailable."), 404

def read_csv_payload():
    if not request.is_json:
        return None, None, (jsonify(error="Expected a JSON request."), 400)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, None, (jsonify(error="Invalid request body."), 400)
    csv_text = payload.get("csv")
    filename = payload.get("filename", "uploaded_billing.csv")
    if not isinstance(csv_text, str) or not isinstance(filename, str):
        return None, None, (jsonify(error="CSV content and filename must be text."), 400)
    if len(csv_text.encode("utf-8")) > MAX_UPLOAD_SIZE:
        return None, None, (jsonify(error="CSV exceeds the 10 MB upload limit."), 413)
    return csv_text, filename, None

def analyze_payload():
    csv_text, filename, error = read_csv_payload()
    if error:
        return None, error
    try:
        result = CloudCostLinter().lint_content(csv_text, source_name=filename)
        return (result, None)
    except CloudCostLinterError as exc:
        return None, (jsonify(error=str(exc)), 400)
    except Exception:
        app.logger.exception("Unexpected billing analysis failure")
        return None, (jsonify(error="Analysis failed due to an internal server error."), 500)

@app.post("/api/analyze")
def analyze():
    result, error = analyze_payload()
    return error if error else jsonify(result)

@app.post("/api/export-csv")
def export_csv():
    result, error = analyze_payload()
    if error:
        return error
    report = CloudCostLinter().generate_csv_report(result)
    filename = request.get_json()["filename"]
    return Response(report, mimetype="text/csv",
                    headers={"Content-Disposition": f'attachment; filename="cloud_cost_analysis_{_safe_download_stem(filename)}.csv"'})

@app.post("/api/export-json")
def export_json():
    result, error = analyze_payload()
    if error:
        return error
    filename = request.get_json()["filename"]
    return Response(json.dumps(result, indent=2), mimetype="application/json",
                    headers={"Content-Disposition": f'attachment; filename="cloud_cost_analysis_{_safe_download_stem(filename)}.json"'})
