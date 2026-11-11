#!/usr/bin/env python3
"""
Automated Test Suite for Cloud Cost Linter
==========================================
Includes independent quality audit tests:
- Edge case: Negative credits and accounting parenthesis notation ($50.00)
- Edge case: Uniform distribution false-positive prevention
- Edge case: Zero cost free-tier items
- Requirement: Distinction between duplicate charges and confirmed refunds
- Requirement: 40% rightsizing verified as an illustrative assumption
- Core functionality: duplicates, outliers, totals, error handling, CLI execution

Uses Python standard library (unittest) only.
"""

import unittest
import tempfile
import os
import subprocess
import json
import threading
import urllib.request
import urllib.error
from http.server import HTTPServer
from cloud_cost_linter import CloudCostLinter, InvalidBillingDataError, CloudCostLinterError
from cloud_cost_linter_web import CloudCostLinterHTTPHandler, MAX_UPLOAD_SIZE


class TestCloudCostLinter(unittest.TestCase):
    """Unit tests for the CloudCostLinter core engine."""

    def setUp(self):
        self.linter = CloudCostLinter(expensive_percentile=85.0, z_score_threshold=1.5)
        self.sample_csv_path = "sample_billing.csv"

    def test_load_sample_csv(self):
        """Verify that sample_billing.csv loads cleanly with 20 records."""
        records = self.linter.load_csv(self.sample_csv_path)
        self.assertEqual(len(records), 20)
        self.assertEqual(records[0]["record_id"], "rec_1001")
        self.assertEqual(records[0]["service"], "Compute Engine")
        self.assertAlmostEqual(records[0]["cost"], 142.50)

    def test_detect_duplicates(self):
        """Verify detection of duplicate billing records and unconfirmed refund status."""
        records = self.linter.load_csv(self.sample_csv_path)
        duplicates = self.linter.detect_duplicates(records)

        # In sample_billing.csv, rec_1004 duplicates rec_1003 ($210.00), rec_1013 duplicates rec_1012 ($89.00)
        self.assertEqual(len(duplicates), 2)

        duplicate_ids = [d["duplicate_record_id"] for d in duplicates]
        self.assertIn("rec_1004", duplicate_ids)
        self.assertIn("rec_1013", duplicate_ids)

        # Quality Requirement: Must explicitly label that refund is unconfirmed
        for d in duplicates:
            self.assertFalse(d["is_confirmed_refund"])
            self.assertIn("Subject to cloud provider dispute", d["explanation"])

        # Check mapping
        dup_1004 = next(d for d in duplicates if d["duplicate_record_id"] == "rec_1004")
        self.assertEqual(dup_1004["original_record_id"], "rec_1003")
        self.assertAlmostEqual(dup_1004["cost"], 210.00)

    def test_calculate_total_spending(self):
        """Verify accurate total spend calculation and service aggregations."""
        records = self.linter.load_csv(self.sample_csv_path)
        spending = self.linter.calculate_total_spending(records)

        # Total calculated from sample_billing.csv
        expected_total = (
            142.50 + 142.50 + 210.00 + 210.00 + 24.80 + 5.00 + 4820.00 + 32.40 +
            3450.00 + 18.75 + 6.20 + 89.00 + 89.00 + 45.20 + 18.00 + 12.50 +
            65.00 + 0.60 + 14.30 + 2180.00
        )
        self.assertAlmostEqual(spending["total_spending"], round(expected_total, 2))
        self.assertEqual(spending["record_count"], 20)
        self.assertAlmostEqual(spending["spending_by_service"]["Compute Engine"], 5215.20)

    def test_detect_expensive_services(self):
        """Verify statistical outlier detection for unusually expensive services."""
        records = self.linter.load_csv(self.sample_csv_path)
        expensive = self.linter.detect_expensive_services(records)

        self.assertGreater(len(expensive), 0)
        expensive_ids = [e["resource_id"] for e in expensive]

        # The GPU instance ($4,820.00), storage volume ($3,450.00), and egress anomaly ($2,180.00)
        self.assertIn("instance-gpu-training-runaway", expensive_ids)
        self.assertIn("disk-legacy-backup-volume", expensive_ids)

        top_outlier = expensive[0]
        self.assertEqual(top_outlier["resource_id"], "instance-gpu-training-runaway")
        self.assertEqual(top_outlier["cost"], 4820.00)
        self.assertEqual(top_outlier["severity"], "CRITICAL")

    def test_identify_potential_savings_and_disclaimers(self):
        """Verify that savings separate illustrative rightsizing ($3,308) from duplicate charges ($299) without summing."""
        records = self.linter.load_csv(self.sample_csv_path)
        duplicates = self.linter.detect_duplicates(records)
        expensive = self.detect_expensive_services = self.linter.detect_expensive_services(records)
        savings = self.linter.identify_potential_savings(records, duplicates, expensive)

        # Potential duplicate amount ($210 + $89 = $299.00)
        self.assertAlmostEqual(savings["potential_duplicate_charges"], 299.00)
        # Illustrative rightsizing amount ($1,928 + $1,380 = $3,308.00)
        self.assertAlmostEqual(savings["illustrative_rightsizing_projection"], 3308.00)
        self.assertAlmostEqual(savings["verified_savings"], 0.00)

        # Quality Requirement: Must not be verified savings and must include financial separation notice
        self.assertFalse(savings["assumptions"]["is_verified_savings"])
        self.assertIn("illustrative rightsizing estimate only", savings["assumptions"]["disclaimer"].lower())
        self.assertIn("unconfirmed candidate duplicate charges", savings["assumptions"]["disclaimer"].lower())

    # -------------------------------------------------------------
    # NEW EDGE CASE AUDIT TESTS (Developer QA)
    # -------------------------------------------------------------

    def test_edge_case_negative_accounting_costs(self):
        """Verify handling of accounting parenthesis notation ($50.00) and negative credits -$20.00."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
            tmp.write(
                "record_id,service,resource_id,date,cost\n"
                "rec_1,GCP,vm-1,2026-10-01,100.00\n"
                "rec_2,Credit,promo-credit,2026-10-01,($30.00)\n"
                "rec_3,Credit,discount-credit,2026-10-01,-20.00\n"
            )
            tmp_path = tmp.name

        try:
            records = self.linter.load_csv(tmp_path)
            self.assertEqual(len(records), 3)
            self.assertAlmostEqual(records[0]["cost"], 100.00)
            self.assertAlmostEqual(records[1]["cost"], -30.00)
            self.assertAlmostEqual(records[2]["cost"], -20.00)

            spending = self.linter.calculate_total_spending(records)
            self.assertAlmostEqual(spending["total_spending"], 50.00) # 100 - 30 - 20
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_edge_case_uniform_distribution_false_positive_prevention(self):
        """Verify that a uniform dataset (e.g. 10 VMs costing $10.00 to $10.05) produces 0 anomalies."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
            lines = ["record_id,service,resource_id,date,cost"]
            for i in range(10):
                lines.append(f"rec_{i},Compute,vm-{i},2026-10-01,{10.00 + (i * 0.01):.2f}")
            tmp.write("\n".join(lines))
            tmp_path = tmp.name

        try:
            records = self.linter.load_csv(tmp_path)
            expensive = self.linter.detect_expensive_services(records)
            # In a uniform distribution with negligible variance, NO outliers should be flagged
            self.assertEqual(len(expensive), 0)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_edge_case_zero_cost_free_tier(self):
        """Verify handling of $0.00 free tier charges."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
            tmp.write(
                "record_id,service,resource_id,date,cost\n"
                "rec_1,Cloud Functions,fn-webhook,2026-10-01,0.00\n"
                "rec_2,Cloud Functions,fn-health,2026-10-01,$0.00\n"
            )
            tmp_path = tmp.name

        try:
            records = self.linter.load_csv(tmp_path)
            self.assertEqual(records[0]["cost"], 0.0)
            self.assertEqual(records[1]["cost"], 0.0)
            spending = self.linter.calculate_total_spending(records)
            self.assertEqual(spending["total_spending"], 0.0)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_missing_file_error_handling(self):
        """Verify clear FileNotFoundError when billing file does not exist."""
        with self.assertRaises(FileNotFoundError) as ctx:
            self.linter.load_csv("non_existent_billing_file_xyz.csv")
        self.assertIn("not found", str(ctx.exception))

    def test_missing_required_columns(self):
        """Verify InvalidBillingDataError when required columns are absent."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
            tmp.write("resource_name,amount,notes\nres1,50.0,test\n")
            tmp_path = tmp.name

        try:
            with self.assertRaises(InvalidBillingDataError) as ctx:
                self.linter.load_csv(tmp_path)
            self.assertIn("Missing required billing columns", str(ctx.exception))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_non_finite_cost_values_rejected(self):
        """Reject NaN and infinity values so calculations cannot be poisoned."""
        for value in ("nan", "NaN", "inf", "Infinity", "-inf"):
            with self.subTest(value=value):
                csv_text = (
                    "record_id,service,resource_id,date,cost\n"
                    f"rec_1,GCP,res_1,2026-10-01,{value}\\n"
                )
                with self.assertRaises(InvalidBillingDataError):
                    self.linter.load_csv_content(csv_text)

    def test_non_numeric_cost_error(self):
        """Verify InvalidBillingDataError when cost contains non-numeric strings."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
            tmp.write("record_id,service,resource_id,date,cost\nrec_1,GCP,res_1,2026-10-01,FREE_TIER_OVERAGE\n")
            tmp_path = tmp.name

        try:
            with self.assertRaises(InvalidBillingDataError) as ctx:
                self.linter.load_csv(tmp_path)
            self.assertIn("Invalid numeric cost value", str(ctx.exception))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_empty_file_error(self):
        """Verify InvalidBillingDataError when CSV is empty."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".csv") as tmp:
            tmp_path = tmp.name

        try:
            with self.assertRaises(InvalidBillingDataError) as ctx:
                self.linter.load_csv(tmp_path)
            self.assertIn("empty", str(ctx.exception).lower())
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_cli_execution_text(self):
        """Verify running the script via command line outputs formatted report with disclaimers."""
        result = subprocess.run(
            ["python3", "cloud_cost_linter.py", self.sample_csv_path],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("CLOUD COST LINTER REPORT", result.stdout)
        self.assertIn("Potential Duplicate Charges:", result.stdout)
        self.assertIn("Illustrative Rightsizing Estimate", result.stdout)
        self.assertIn("Billing data alone CANNOT determine whether a resource is idle", result.stdout)

    @classmethod
    def setUpClass(cls):
        """Spins up a lightweight local HTTPServer for automated web endpoint testing."""
        cls.server = HTTPServer(("127.0.0.1", 0), CloudCostLinterHTTPHandler)
        cls.server_port = cls.server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{cls.server_port}"
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        """Shuts down test local HTTPServer."""
        cls.server.shutdown()
        cls.server.server_close()

    def test_cli_execution_json(self):
        """Verify CLI --json flag produces valid, parseable JSON with assumptions metadata."""
        result = subprocess.run(
            ["python3", "cloud_cost_linter.py", self.sample_csv_path, "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        parsed = json.loads(result.stdout)
        self.assertIn("summary", parsed)
        self.assertEqual(parsed["summary"]["potential_duplicate_count"], 2)
        self.assertIn("potential_savings", parsed)
        self.assertIn("assumptions", parsed["potential_savings"])
        self.assertFalse(parsed["potential_savings"]["assumptions"]["is_verified_savings"])

    # -------------------------------------------------------------
    # MISSION 002 PRODUCT UPGRADE & LOCAL WEB INTERFACE TESTS
    # -------------------------------------------------------------

    def test_load_csv_content_memory(self):
        """Verify in-memory string CSV parsing without requiring disk files."""
        with open(self.sample_csv_path, "r", encoding="utf-8") as f:
            content = f.read()

        records = self.linter.load_csv_content(content, source_name="memory_test.csv")
        self.assertEqual(len(records), 20)
        self.assertEqual(records[0]["record_id"], "rec_1001")
        self.assertAlmostEqual(records[0]["cost"], 142.50)

    def test_lint_content_memory(self):
        """Verify complete linting pipeline executed entirely in memory."""
        with open(self.sample_csv_path, "r", encoding="utf-8") as f:
            content = f.read()

        results = self.linter.lint_content(content, source_name="memory_test.csv")
        self.assertEqual(results["file"], "memory_test.csv")
        self.assertAlmostEqual(results["summary"]["total_spending"], 11575.75)
        self.assertEqual(results["summary"]["potential_duplicate_count"], 2)
        self.assertAlmostEqual(results["summary"]["potential_duplicate_charges"], 299.00)
        self.assertAlmostEqual(results["summary"]["illustrative_rightsizing_projection"], 3308.00)
        self.assertFalse(results["potential_savings"]["assumptions"]["is_verified_savings"])

    def test_generate_csv_report_structure(self):
        """Verify generation of downloadable, structured CSV analysis report with all disclaimers."""
        results = self.linter.lint(self.sample_csv_path)
        report_csv = self.linter.generate_csv_report(results)

        self.assertIn("=== CLOUD COST LINTER AUDIT REPORT ===", report_csv)
        self.assertIn("$11,575.75", report_csv)
        self.assertIn("=== POTENTIAL DUPLICATE CHARGES", report_csv)
        self.assertIn("rec_1004", report_csv)
        self.assertIn("=== STATISTICALLY EXPENSIVE SERVICES & ANOMALIES ===", report_csv)
        self.assertIn("instance-gpu-training-runaway", report_csv)
        self.assertIn("Verified Realized Savings (USD),$0.00 (Verified Realized Savings)", report_csv)
        self.assertIn("=== METHODOLOGY & AUDIT DISCLAIMERS ===", report_csv)
        self.assertIn("Billing data alone CANNOT determine whether a resource is idle", report_csv)

    def test_file_size_validation_oversized(self):
        """Verify rejection of oversized payloads exceeding the 10MB limit."""
        # Create string exceeding 10 MB limit
        oversized_str = "record_id,service,resource_id,date,cost\n" + ("x" * (MAX_UPLOAD_SIZE + 1024))
        with self.assertRaises(InvalidBillingDataError) as ctx:
            self.linter.load_csv_content(oversized_str, source_name="huge_file.csv")
        self.assertIn("exceeds maximum allowed limit", str(ctx.exception))

    def test_file_type_validation_invalid_extension(self):
        """Verify rejection of non-CSV extensions (.sh, .py, .exe)."""
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".sh") as tmp:
            tmp.write("#!/bin/bash\necho dangerous")
            tmp_path = tmp.name

        try:
            with self.assertRaises(InvalidBillingDataError) as ctx:
                self.linter.validate_file_path(tmp_path)
            self.assertIn("Invalid file extension", str(ctx.exception))
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_web_server_get_index_html(self):
        """Verify GET / returns HTTP 200 with local web interface HTML and privacy notices."""
        req = urllib.request.Request(f"{self.base_url}/")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/html", resp.headers.get("Content-Type", ""))
            self.assertEqual(resp.headers.get("X-Content-Type-Options"), "nosniff")
            self.assertEqual(resp.headers.get("X-Frame-Options"), "DENY")
            self.assertEqual(resp.headers.get("Referrer-Policy"), "no-referrer")
            self.assertIn("frame-ancestors 'none'", resp.headers.get("Content-Security-Policy", ""))
            html = resp.read().decode("utf-8")
            self.assertIn("Cloud Cost Linter", html)
            self.assertIn("100% Local · Zero Telemetry", html)
            self.assertIn("Select or Drop Your Cloud Billing CSV", html)

    def test_web_server_head_request(self):
        """Verify HEAD / returns HTTP 200 with matching headers but strictly zero response body."""
        req = urllib.request.Request(f"{self.base_url}/", method="HEAD")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/html", resp.headers.get("Content-Type", ""))
            content_length = int(resp.headers.get("Content-Length", "0"))
            self.assertGreater(content_length, 0)
            body = resp.read()
            self.assertEqual(len(body), 0)

    def test_web_server_get_sample_data(self):
        """Verify GET /api/sample returns HTTP 200 and valid CSV data."""
        req = urllib.request.Request(f"{self.base_url}/api/sample")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/csv", resp.headers.get("Content-Type", ""))
            body = resp.read().decode("utf-8")
            self.assertIn("record_id,service,resource_id,date,cost", body)
            self.assertIn("rec_1001", body)

    def test_web_server_get_health(self):
        """Verify GET /api/health returns HTTP 200 and health metadata."""
        req = urllib.request.Request(f"{self.base_url}/api/health")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data["status"], "ok")
            self.assertIn("100% Local-First", data["privacy"])

    def test_web_server_post_analyze_valid(self):
        """Verify POST /api/analyze processes valid CSV and returns analysis JSON."""
        with open(self.sample_csv_path, "r", encoding="utf-8") as f:
            csv_text = f.read()

        payload = json.dumps({"csv": csv_text, "filename": "sample_billing.csv"}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/analyze",
            data=payload,
            headers={"Content-Type": "application/json", "Content-Length": str(len(payload))},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertAlmostEqual(data["summary"]["total_spending"], 11575.75)
            self.assertEqual(data["summary"]["potential_duplicate_count"], 2)
            self.assertAlmostEqual(data["summary"]["potential_duplicate_charges"], 299.00)
            self.assertAlmostEqual(data["summary"]["illustrative_rightsizing_projection"], 3308.00)
            self.assertFalse(data["potential_savings"]["assumptions"]["is_verified_savings"])

    def test_web_server_post_analyze_invalid_numeric_cost(self):
        """Verify invalid numeric costs return a complete JSON error response."""
        bad_csv = "record_id,service,resource_id,date,cost\nINV001,EC2,server-001,2026-11-04,INVALID\n"
        payload = json.dumps({"csv": bad_csv, "filename": "invalid-test.csv"}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/analyze",
            data=payload,
            headers={"Content-Type": "application/json", "Content-Length": str(len(payload))},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(ctx.exception.headers.get("Connection"), "close")
        err_body = ctx.exception.read().decode("utf-8")
        parsed = json.loads(err_body)
        self.assertIn("Invalid numeric cost value", parsed["error"])

    def test_web_server_post_analyze_invalid_csv(self):
        """Verify POST /api/analyze returns HTTP 400 on malformed CSV missing required headers."""
        bad_csv = "res_name,cost_usd,category\nvm-1,50.0,Compute\n"
        payload = json.dumps({"csv": bad_csv, "filename": "bad.csv"}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/analyze",
            data=payload,
            headers={"Content-Type": "application/json", "Content-Length": str(len(payload))},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)
        err_body = json.loads(ctx.exception.read().decode("utf-8"))
        self.assertIn("Missing required billing columns", err_body["error"])

    def test_web_server_post_analyze_oversized(self):
        """Verify POST /api/analyze returns HTTP 413 Payload Too Large on oversized upload."""
        oversized_len = MAX_UPLOAD_SIZE + 2048
        # Send header claiming oversized payload
        req = urllib.request.Request(
            f"{self.base_url}/api/analyze",
            data=b"",
            headers={"Content-Type": "application/json", "Content-Length": str(oversized_len)},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 413)

    def test_web_server_export_csv(self):
        """Verify POST /api/export-csv returns downloadable CSV analysis attachment."""
        with open(self.sample_csv_path, "r", encoding="utf-8") as f:
            csv_text = f.read()

        payload = json.dumps({"csv": csv_text, "filename": "sample_billing.csv"}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/export-csv",
            data=payload,
            headers={"Content-Type": "application/json", "Content-Length": str(len(payload))},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("text/csv", resp.headers.get("Content-Type", ""))
            self.assertIn("attachment", resp.headers.get("Content-Disposition", ""))
            csv_data = resp.read().decode("utf-8")
            self.assertIn("=== CLOUD COST LINTER AUDIT REPORT ===", csv_data)
            self.assertIn("$11,575.75", csv_data)

    def test_web_server_export_json(self):
        """Verify POST /api/export-json returns downloadable JSON analysis attachment."""
        with open(self.sample_csv_path, "r", encoding="utf-8") as f:
            csv_text = f.read()

        payload = json.dumps({"csv": csv_text, "filename": "sample_billing.csv"}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/export-json",
            data=payload,
            headers={"Content-Type": "application/json", "Content-Length": str(len(payload))},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            self.assertIn("application/json", resp.headers.get("Content-Type", ""))
            self.assertIn("attachment", resp.headers.get("Content-Disposition", ""))
            parsed = json.loads(resp.read().decode("utf-8"))
            self.assertIn("summary", parsed)
            self.assertAlmostEqual(parsed["summary"]["total_spending"], 11575.75)


    def test_csv_report_neutralizes_spreadsheet_formula_cells(self):
        """Untrusted text fields must not be interpreted as spreadsheet formulas."""
        results = self.linter.lint_content(
            open(self.sample_csv_path, "r", encoding="utf-8").read(),
            source_name="=HYPERLINK('https://example.invalid','open')",
        )
        results["spending_breakdown"]["spending_by_service"] = {
            "@SUM(1,1)": 1.0,
            "Normal Service": 2.0,
        }
        results["duplicates"] = [{
            "duplicate_record_id": "+CMD|' /C calc'!A0",
            "original_record_id": "-1+1",
            "service": "=2+2",
            "resource_id": "\t=HYPERLINK('https://example.invalid')",
            "date": "2026-11-11",
            "cost": 1.0,
            "explanation": "@SUM(1,1)",
        }]
        results["expensive_services"] = []
        results["potential_savings"]["recommendations"] = []

        report = self.linter.generate_csv_report(results)

        self.assertIn("'=HYPERLINK", report)
        self.assertIn("'@SUM(1,1)", report)
        self.assertIn("'+CMD", report)
        self.assertIn("'-1+1", report)
        self.assertIn("'=2+2", report)
        self.assertIn("'\t=HYPERLINK", report)
        self.assertIn("Normal Service", report)

    def test_export_filename_is_sanitized_and_cors_is_not_wildcard(self):
        """Untrusted upload names must not inject response headers or paths."""
        with open(self.sample_csv_path, "r", encoding="utf-8") as f:
            csv_text = f.read()

        payload = json.dumps({
            "csv": csv_text,
            "filename": "../../evil\\r\\nX-Injected: yes.csv",
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/export-csv",
            data=payload,
            headers={"Content-Type": "application/json", "Content-Length": str(len(payload))},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            disposition = resp.headers.get("Content-Disposition", "")
            self.assertIn("attachment;", disposition)
            self.assertNotIn("\r", disposition)
            self.assertNotIn("\n", disposition)
            self.assertIn('filename="cloud_cost_analysis_', disposition)
            self.assertTrue(disposition.endswith('.csv"'))
            self.assertNotIn("..", disposition)
            self.assertNotIn("/", disposition)
            self.assertNotIn("Access-Control-Allow-Origin", resp.headers)

    def test_json_payload_must_be_object_with_string_csv(self):
        """Reject malformed JSON API shapes instead of processing arbitrary values."""
        payload = json.dumps(["not", "an", "object"]).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/analyze",
            data=payload,
            headers={"Content-Type": "application/json", "Content-Length": str(len(payload))},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
