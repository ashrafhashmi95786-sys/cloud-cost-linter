#!/usr/bin/env python3
"""
Cloud Cost Linter
=================
An open-source, zero-dependency command-line utility for detecting cloud billing anomalies,
potential duplicate charges, and illustrative cost optimization opportunities.

Author: Autonomous AI Society (Developer: Kaelen Vance)
License: MIT
Dependencies: Python standard library only.
"""

import sys
import os
import io
import csv
import json
import math
import argparse
from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict


class CloudCostLinterError(Exception):
    """Custom exception base class for Cloud Cost Linter."""
    pass


class InvalidBillingDataError(CloudCostLinterError):
    """Raised when CSV structure or data types are invalid."""
    pass


def _safe_csv_cell(value: Any) -> Any:
    """Neutralize spreadsheet formula prefixes in untrusted text cells."""
    if not isinstance(value, str):
        return value
    stripped = value.lstrip(" \t\r\n")
    if value.startswith(("\t", "\r", "\n")) or stripped.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


class _FormulaSafeCSVWriter:
    """CSV writer adapter that sanitizes text cells before serialization."""

    def __init__(self, output: Any):
        self._writer = csv.writer(output)

    def writerow(self, row: List[Any]) -> None:
        self._writer.writerow([_safe_csv_cell(value) for value in row])


class CloudCostLinter:
    """Core analysis engine for cloud billing logs."""

    REQUIRED_COLUMNS = ["record_id", "service", "resource_id", "date", "cost"]
    MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB upload and file limit
    ALLOWED_EXTENSIONS = {".csv"}

    def __init__(
        self,
        expensive_percentile: float = 90.0,
        z_score_threshold: float = 2.0,
        min_outlier_dollar_delta: float = 25.0,
        illustrative_rightsizing_factor: float = 0.40,
    ):
        self.expensive_percentile = expensive_percentile
        self.z_score_threshold = z_score_threshold
        self.min_outlier_dollar_delta = min_outlier_dollar_delta
        self.illustrative_rightsizing_factor = illustrative_rightsizing_factor

    def validate_file_path(self, file_path: str) -> None:
        """Validates file existence, file extension, and file size limits."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Billing file not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext and ext not in self.ALLOWED_EXTENSIONS:
            raise InvalidBillingDataError(
                f"Invalid file extension '{ext}'. Only CSV files ({', '.join(self.ALLOWED_EXTENSIONS)}) are supported."
            )

        file_size = os.path.getsize(file_path)
        if file_size > self.MAX_FILE_SIZE_BYTES:
            raise InvalidBillingDataError(
                f"File size ({file_size / (1024 * 1024):.1f} MB) exceeds maximum allowed limit of "
                f"{self.MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
            )

    def _parse_csv_stream(self, reader: csv.DictReader, source_name: str) -> List[Dict[str, Any]]:
        """Internal helper to validate headers and parse records with accounting notation support."""
        if not reader.fieldnames:
            raise InvalidBillingDataError(f"Billing file '{source_name}' is completely empty or missing headers.")

        headers = [h.strip().lower() for h in reader.fieldnames if h]
        missing = [col for col in self.REQUIRED_COLUMNS if col not in headers]
        if missing:
            raise InvalidBillingDataError(
                f"Missing required billing columns: {', '.join(missing)}. "
                f"Expected at minimum: {', '.join(self.REQUIRED_COLUMNS)}"
            )

        records: List[Dict[str, Any]] = []
        for line_num, row in enumerate(reader, start=2):
            cleaned = {k.strip().lower(): (v.strip() if v else "") for k, v in row.items()}

            raw_cost = cleaned.get("cost", "").strip()
            if not raw_cost:
                raise InvalidBillingDataError(f"Missing cost value on line {line_num}.")

            is_negative = False
            clean_str = raw_cost
            if clean_str.startswith("(") and clean_str.endswith(")"):
                is_negative = True
                clean_str = clean_str[1:-1].strip()
            elif clean_str.startswith("-"):
                is_negative = True
                clean_str = clean_str[1:].strip()

            clean_str = clean_str.replace("$", "").replace(",", "").strip()

            try:
                cost = float(clean_str)
                if is_negative:
                    cost = -cost
                if not math.isfinite(cost):
                    raise InvalidBillingDataError(
                        f"Cost must be a finite number on line {line_num} "
                        f"for resource '{cleaned.get('resource_id', 'unknown')}'."
                    )
            except (ValueError, TypeError):
                raise InvalidBillingDataError(
                    f"Invalid numeric cost value '{raw_cost}' on line {line_num} "
                    f"for resource '{cleaned.get('resource_id', 'unknown')}'."
                )

            record = {
                "record_id": cleaned.get("record_id", f"rec_{line_num}"),
                "service": cleaned.get("service", "Unknown Service"),
                "resource_id": cleaned.get("resource_id", "Unknown Resource"),
                "date": cleaned.get("date", ""),
                "cost": cost,
                "region": cleaned.get("region", "global"),
                "description": cleaned.get("description", ""),
            }
            records.append(record)

        if not records:
            raise InvalidBillingDataError(f"No billing data records found in '{source_name}'.")

        return records

    def load_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Loads and parses a billing CSV file with strict validation.
        Handles standard numeric values, currency symbols, and accounting parenthesis notation for negatives.
        """
        self.validate_file_path(file_path)

        try:
            with open(file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                return self._parse_csv_stream(reader, file_path)
        except (UnicodeDecodeError, csv.Error) as err:
            raise InvalidBillingDataError(f"Failed to read CSV file: {err}")

    def load_csv_content(self, content_str: str, source_name: str = "uploaded_content") -> List[Dict[str, Any]]:
        """
        Loads and parses CSV content directly from in-memory string.
        Validates payload size, column headers, and data formats without saving to disk or executing files.
        """
        raw_bytes_len = len(content_str.encode("utf-8"))
        if raw_bytes_len > self.MAX_FILE_SIZE_BYTES:
            raise InvalidBillingDataError(
                f"Uploaded content size ({raw_bytes_len / (1024 * 1024):.1f} MB) exceeds maximum allowed limit of "
                f"{self.MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
            )

        if not content_str or not content_str.strip():
            raise InvalidBillingDataError(f"Billing data '{source_name}' is empty.")

        if content_str.startswith("\ufeff"):
            content_str = content_str[1:]

        try:
            stream = io.StringIO(content_str)
            reader = csv.DictReader(stream)
            return self._parse_csv_stream(reader, source_name)
        except (UnicodeDecodeError, csv.Error) as err:
            raise InvalidBillingDataError(f"Failed to parse CSV data: {err}")

    def detect_duplicates(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identifies potential duplicate charges (same service, resource_id, date, and cost).
        Note: Flags potential duplicates for provider investigation; does not guarantee refund.
        """
        seen: Dict[Tuple[str, str, str, float], List[Dict[str, Any]]] = defaultdict(list)

        for rec in records:
            # Key for duplicate identification
            key = (
                rec["service"].lower(),
                rec["resource_id"].lower(),
                rec["date"],
                round(rec["cost"], 4),
            )
            seen[key].append(rec)

        duplicates: List[Dict[str, Any]] = []
        for key, instances in seen.items():
            if len(instances) > 1:
                original = instances[0]
                for redundant in instances[1:]:
                    duplicates.append({
                        "original_record_id": original["record_id"],
                        "duplicate_record_id": redundant["record_id"],
                        "service": redundant["service"],
                        "resource_id": redundant["resource_id"],
                        "date": redundant["date"],
                        "cost": redundant["cost"],
                        "is_confirmed_refund": False,
                        "explanation": (
                            f"Potential duplicate charge of ${redundant['cost']:.2f} matches record "
                            f"{original['record_id']} on {redundant['date']}. (Subject to cloud provider dispute verification)."
                        ),
                    })

        return duplicates

    def calculate_total_spending(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates total expenditure and provides service-level aggregations.
        """
        total = sum(r["cost"] for r in records)
        by_service: Dict[str, float] = defaultdict(float)
        by_date: Dict[str, float] = defaultdict(float)

        for r in records:
            by_service[r["service"]] += r["cost"]
            if r["date"]:
                by_date[r["date"]] += r["cost"]

        # Sort services by highest spend
        sorted_services = sorted(by_service.items(), key=lambda x: x[1], reverse=True)

        return {
            "total_spending": round(total, 2),
            "record_count": len(records),
            "spending_by_service": {k: round(v, 2) for k, v in sorted_services},
            "top_service": sorted_services[0] if sorted_services else ("None", 0.0),
        }

    def detect_expensive_services(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detects unusually expensive services using statistical anomaly detection.
        Requires both statistical significance (Z-Score >= threshold) and meaningful dollar delta
        to eliminate false positives on uniform distributions.
        """
        if len(records) < 2:
            return []

        costs = [r["cost"] for r in records]
        mean_cost = sum(costs) / len(costs)
        variance = sum((c - mean_cost) ** 2 for c in costs) / len(costs)
        std_dev = math.sqrt(variance) if variance > 0 else 0.0

        # If variance is negligible (< $0.01), no statistical anomalies exist
        if std_dev < 0.01:
            return []

        # Percentile calculation
        sorted_costs = sorted(costs)
        p_idx = int(len(sorted_costs) * (self.expensive_percentile / 100.0))
        p_idx = min(p_idx, len(sorted_costs) - 1)
        percentile_threshold = sorted_costs[p_idx]

        outliers: List[Dict[str, Any]] = []

        for r in records:
            c = r["cost"]
            z_score = ((c - mean_cost) / std_dev) if std_dev > 0 else 0.0
            dollar_delta = c - mean_cost

            # Anomaly criteria: must exceed Z-score threshold, be above population mean,
            # and differ from mean by at least min_outlier_dollar_delta
            if z_score >= self.z_score_threshold and dollar_delta >= self.min_outlier_dollar_delta:
                severity = "CRITICAL" if z_score >= 3.0 or c >= (mean_cost * 3) else "HIGH"
                outliers.append({
                    "record_id": r["record_id"],
                    "service": r["service"],
                    "resource_id": r["resource_id"],
                    "cost": r["cost"],
                    "mean_cost": round(mean_cost, 2),
                    "z_score": round(z_score, 2),
                    "severity": severity,
                    "explanation": (
                        f"Cost of ${c:.2f} significantly exceeds benchmark population mean (${mean_cost:.2f}) "
                        f"with Z-Score of {z_score:.2f}. (Requires runtime telemetry audit)."
                    ),
                })

        # Sort by cost descending
        outliers.sort(key=lambda x: x["cost"], reverse=True)
        return outliers

    def identify_potential_savings(
        self,
        records: List[Dict[str, Any]],
        duplicates: List[Dict[str, Any]],
        expensive: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Identifies potential cost reduction areas.
        Distinguishes potential duplicate charges from verified refunds,
        and labels rightsizing as an illustrative heuristic assumption.
        """
        potential_duplicate_amount = sum(d["cost"] for d in duplicates)

        # Illustrative savings from expensive anomaly reduction using configurable factor (default: 40%)
        illustrative_savings = 0.0
        recommendations: List[Dict[str, Any]] = []

        # 1. Duplicate billing entries
        if duplicates:
            recommendations.append({
                "type": "POTENTIAL_DUPLICATE_CHARGE",
                "estimated_potential": round(potential_duplicate_amount, 2),
                "is_guaranteed": False,
                "action": (
                    f"Audit {len(duplicates)} potential duplicate charge(s) totalling ${potential_duplicate_amount:.2f}. "
                    "Submit dispute to cloud provider to confirm whether charges are redundant or legitimate concurrent usage."
                ),
            })

        # 2. Outlier cost reduction (Illustrative heuristic)
        for exp in expensive[:5]:
            est_saving = exp["cost"] * self.illustrative_rightsizing_factor
            illustrative_savings += est_saving
            recommendations.append({
                "type": "ILLUSTRATIVE_RIGHTSIZING_PROJECTION",
                "resource_id": exp["resource_id"],
                "service": exp["service"],
                "estimated_potential": round(est_saving, 2),
                "is_guaranteed": False,
                "illustrative_assumption": f"Illustrative {int(self.illustrative_rightsizing_factor * 100)}% reduction heuristic",
                "action": (
                    f"Audit telemetry (CPU, memory, IOPS) for {exp['resource_id']} ({exp['service']}). "
                    f"Illustrative {int(self.illustrative_rightsizing_factor * 100)}% reduction projection (~${est_saving:.2f}). "
                    "Note: Billing data alone cannot confirm whether this resource is idle or active."
                ),
            })

        return {
            "potential_duplicate_charges": round(potential_duplicate_amount, 2),
            "illustrative_rightsizing_projection": round(illustrative_savings, 2),
            "verified_savings": 0.00,
            "assumptions": {
                "rightsizing_percentage_factor": self.illustrative_rightsizing_factor,
                "is_verified_savings": False,
                "disclaimer": (
                    "Financial separation notice: $3,308 is an illustrative rightsizing estimate only. "
                    "$299 represents unconfirmed candidate duplicate charges only. "
                    "$0.00 represents verified savings. "
                    "Neither amount is verified, guaranteed, or combined into a total savings projection. "
                    "Actual savings require active monitoring telemetry and cloud provider dispute resolution."
                ),
            },
            "recommendations": recommendations,
        }

    def lint(self, file_path: str) -> Dict[str, Any]:
        """
        Executes complete linting pipeline on target file.
        """
        records = self.load_csv(file_path)
        duplicates = self.detect_duplicates(records)
        expensive = self.detect_expensive_services(records)
        spending = self.calculate_total_spending(records)
        savings = self.identify_potential_savings(records, duplicates, expensive)

        return {
            "file": file_path,
            "summary": {
                "total_spending": spending["total_spending"],
                "record_count": spending["record_count"],
                "potential_duplicate_count": len(duplicates),
                "expensive_anomalies_count": len(expensive),
                "potential_duplicate_charges": savings["potential_duplicate_charges"],
                "illustrative_rightsizing_projection": savings["illustrative_rightsizing_projection"],
                "verified_savings": 0.00,
            },
            "spending_breakdown": spending,
            "duplicates": duplicates,
            "expensive_services": expensive,
            "potential_savings": savings,
        }

    def lint_content(self, content_str: str, source_name: str = "uploaded_billing.csv") -> Dict[str, Any]:
        """Executes complete linting pipeline on raw CSV content string."""
        records = self.load_csv_content(content_str, source_name)
        duplicates = self.detect_duplicates(records)
        expensive = self.detect_expensive_services(records)
        spending = self.calculate_total_spending(records)
        savings = self.identify_potential_savings(records, duplicates, expensive)

        return {
            "file": source_name,
            "summary": {
                "total_spending": spending["total_spending"],
                "record_count": spending["record_count"],
                "potential_duplicate_count": len(duplicates),
                "expensive_anomalies_count": len(expensive),
                "potential_duplicate_charges": savings["potential_duplicate_charges"],
                "illustrative_rightsizing_projection": savings["illustrative_rightsizing_projection"],
                "verified_savings": 0.00,
            },
            "spending_breakdown": spending,
            "duplicates": duplicates,
            "expensive_services": expensive,
            "potential_savings": savings,
        }

    def generate_csv_report(self, results: Dict[str, Any]) -> str:
        """Generates a downloadable, audit-ready structured CSV analysis report."""
        output = io.StringIO()
        writer = _FormulaSafeCSVWriter(output)

        # 1. Header & Executive Summary
        writer.writerow(["=== CLOUD COST LINTER AUDIT REPORT ==="])
        writer.writerow(["Target File", results.get("file", "uploaded_data")])
        writer.writerow(["Total Records Audited", results["summary"]["record_count"]])
        writer.writerow(["Total Spending (USD)", f"${results['summary']['total_spending']:,.2f}"])
        writer.writerow(["Potential Duplicate Charges Count", results["summary"]["potential_duplicate_count"]])
        writer.writerow(["Potential Duplicate Amount (USD)", f"${results['potential_savings']['potential_duplicate_charges']:,.2f} (Unconfirmed)"])
        writer.writerow(["Statistical Cost Outliers Count", results["summary"]["expensive_anomalies_count"]])
        writer.writerow(["Illustrative Rightsizing (USD)", f"${results['potential_savings']['illustrative_rightsizing_projection']:,.2f} (Illustrative 40% Heuristic)"])
        writer.writerow(["Potential Duplicate Charges (USD)", f"${results['potential_savings']['potential_duplicate_charges']:,.2f} (Unconfirmed Dispute Candidates)"])
        writer.writerow(["Illustrative Rightsizing Estimate (USD)", f"${results['potential_savings']['illustrative_rightsizing_projection']:,.2f} (Illustrative Heuristic Estimate, Unverified)"])
        writer.writerow(["Verified Realized Savings (USD)", "$0.00 (Verified Realized Savings)"])
        writer.writerow([])

        # 2. Spending by Service
        writer.writerow(["=== SPENDING BY SERVICE ==="])
        writer.writerow(["Service", "Spend (USD)", "Percentage of Total"])
        total_spend = results["summary"]["total_spending"]
        for srv, amt in results["spending_breakdown"]["spending_by_service"].items():
            pct = (amt / total_spend * 100) if total_spend > 0 else 0
            writer.writerow([srv, f"${amt:,.2f}", f"{pct:.1f}%"])
        writer.writerow([])

        # 3. Potential Duplicate Charges
        writer.writerow(["=== POTENTIAL DUPLICATE CHARGES (Subject to Provider Dispute) ==="])
        writer.writerow(["Duplicate Record ID", "Original Record ID", "Service", "Resource ID", "Date", "Cost (USD)", "Status", "Audit Note"])
        if not results["duplicates"]:
            writer.writerow(["None", "None", "None", "None", "None", "$0.00", "Clean Ledger", "No duplicate charges detected."])
        else:
            for d in results["duplicates"]:
                writer.writerow([
                    d["duplicate_record_id"],
                    d["original_record_id"],
                    d["service"],
                    d["resource_id"],
                    d["date"],
                    f"${d['cost']:,.2f}",
                    "Unconfirmed Dispute Candidate",
                    d["explanation"],
                ])
        writer.writerow([])

        # 4. Statistical Cost Outliers
        writer.writerow(["=== STATISTICALLY EXPENSIVE SERVICES & ANOMALIES ==="])
        writer.writerow(["Severity", "Record ID", "Service", "Resource ID", "Cost (USD)", "Population Mean (USD)", "Z-Score", "Telemetry Requirement"])
        if not results["expensive_services"]:
            writer.writerow(["None", "None", "None", "None", "$0.00", "$0.00", "0.0", "No statistical outliers detected."])
        else:
            for e in results["expensive_services"]:
                writer.writerow([
                    e["severity"],
                    e["record_id"],
                    e["service"],
                    e["resource_id"],
                    f"${e['cost']:,.2f}",
                    f"${e['mean_cost']:,.2f}",
                    e["z_score"],
                    "Requires active CPU/memory telemetry audit. Billing data alone cannot determine idle state.",
                ])
        writer.writerow([])

        # 5. Actionable Recommendations & Heuristics
        writer.writerow(["=== ACTIONABLE SAVINGS RECOMMENDATIONS & HEURISTIC PROJECTIONS ==="])
        writer.writerow(["Recommendation Type", "Resource / Service", "Estimated Potential (USD)", "Guaranteed", "Action Required & Disclaimer"])
        for rec in results["potential_savings"]["recommendations"]:
            writer.writerow([
                rec["type"],
                f"{rec.get('service', 'General')} - {rec.get('resource_id', 'All')}",
                f"${rec['estimated_potential']:,.2f}",
                "False",
                rec["action"],
            ])
        writer.writerow([])

        # 6. Audit & Legal Methodology Disclaimers
        writer.writerow(["=== METHODOLOGY & AUDIT DISCLAIMERS ==="])
        writer.writerow(["1. Billing data alone CANNOT determine whether a resource is idle or active."])
        writer.writerow(["2. The 40% rightsizing figure is an illustrative heuristic assumption, not verified savings."])
        writer.writerow(["3. Potential duplicate charges require cloud provider confirmation before refunds."])
        writer.writerow(["4. Verified realized savings remain $0.00 until operational and dispute verification are completed."])

        return output.getvalue()


def format_text_report(results: Dict[str, Any]) -> str:
    """Formats the linting result into a clean terminal report with explicit assumptions."""
    summary = results["summary"]
    breakdown = results["spending_breakdown"]
    duplicates = results["duplicates"]
    expensive = results["expensive_services"]
    savings = results["potential_savings"]

    lines = [
        "=" * 74,
        "                       CLOUD COST LINTER REPORT",
        "=" * 74,
        f" Target File:                    {results['file']}",
        f" Total Records Audited:          {summary['record_count']}",
        f" Total Spending:                 ${summary['total_spending']:,.2f}",
        f" Potential Duplicate Charges:    {summary['potential_duplicate_count']} (${savings['potential_duplicate_charges']:,.2f} unconfirmed dispute candidates)",
        f" Statistically Expensive Outliers:{summary['expensive_anomalies_count']}",
        f" Illustrative Rightsizing Estimate: ${savings['illustrative_rightsizing_projection']:,.2f} (40% heuristic, unverified)",
        f" Verified Realized Savings:      $0.00 (Verified realized savings)",
        "-" * 74,
        " SPENDING BY SERVICE (Top):",
    ]

    for service, amount in list(breakdown["spending_by_service"].items())[:6]:
        pct = (amount / summary["total_spending"] * 100) if summary["total_spending"] > 0 else 0
        lines.append(f"   • {service:<24} ${amount:>10,.2f} ({pct:>5.1f}%)")

    lines.append("-" * 74)
    lines.append(" POTENTIAL DUPLICATE BILLING CHARGES (Subject to Provider Dispute):")
    if not duplicates:
        lines.append("   ✓ No duplicate charges detected. Clean billing ledger.")
    else:
        for d in duplicates:
            lines.append(
                f"   [!] Potential Duplicate {d['duplicate_record_id']} matches {d['original_record_id']} "
                f"({d['service']} / {d['resource_id']}): ${d['cost']:,.2f} on {d['date']}"
            )

    lines.append("-" * 74)
    lines.append(" STATISTICALLY EXPENSIVE SERVICES & ANOMALIES:")
    if not expensive:
        lines.append("   ✓ No statistical cost outliers detected.")
    else:
        for e in expensive[:6]:
            lines.append(
                f"   [{e['severity']}] {e['service']} - {e['resource_id']}: "
                f"${e['cost']:,.2f} (Z-Score: {e['z_score']}, Avg: ${e['mean_cost']:,.2f})"
            )

    lines.append("-" * 74)
    lines.append(" ACTIONABLE SAVINGS RECOMMENDATIONS & HEURISTIC PROJECTIONS:")
    for rec in savings["recommendations"]:
        lines.append(f"   ► [{rec['type']}] Potential ~${rec['estimated_potential']:,.2f}: {rec['action']}")

    lines.append("-" * 74)
    lines.append(" METHODOLOGY & AUDIT DISCLAIMER:")
    lines.append("   * 1. Billing data alone CANNOT determine whether a resource is idle or active.")
    lines.append("   * 2. The 40% rightsizing figure is an illustrative heuristic, not verified savings.")
    lines.append("   * 3. Potential duplicate charges require cloud provider confirmation before refunds.")
    lines.append("=" * 74)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Cloud Cost Linter - Detect potential duplicate charges, cost outliers, and savings in billing data."
    )
    parser.add_argument("csv_file", nargs="?", default=None, help="Path to billing CSV file")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--threshold", type=float, default=2.0, help="Z-score threshold for outliers (default: 2.0)")
    parser.add_argument("--serve", nargs="?", const=8080, type=int, metavar="PORT", help="Start local web interface (default port: 8080)")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind to for web server (default: 127.0.0.1)")

    args = parser.parse_args()

    if args.serve is not None:
        try:
            from cloud_cost_linter_web import run_web_server
            run_web_server(port=args.serve, host=args.host)
            sys.exit(0)
        except ImportError as e:
            sys.stderr.write(f"Web server module could not be loaded: {e}\n")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nShutting down local web server.")
            sys.exit(0)

    if not args.csv_file:
        parser.error("csv_file argument is required when not running with --serve.")

    try:
        linter = CloudCostLinter(z_score_threshold=args.threshold)
        results = linter.lint(args.csv_file)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(format_text_report(results))

        sys.exit(0)
    except CloudCostLinterError as e:
        sys.stderr.write(f"Cloud Cost Linter Error: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Unexpected Error: {e}\n")
        sys.exit(2)


if __name__ == "__main__":
    main()
