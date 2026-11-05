#!/usr/bin/env python3
"""
Cloud Cost Linter - Local Web Interface
========================================
An offline, privacy-first local web interface for analyzing cloud billing CSVs.
Built using Python standard library (http.server) with zero external dependencies.

Privacy Guarantee:
- 100% Local processing on 127.0.0.1.
- No external network calls, no cloud telemetry, no analytics.
- Zero API keys or cloud credentials requested or required.

Author: Autonomous AI Society (Developer: Kaelen Vance, Marketer: Sariha Chen)
License: MIT
"""

import sys
import os
import io
import json
import re
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Dict, Any

# Import core linting engine from cloud_cost_linter.py
try:
    from cloud_cost_linter import CloudCostLinter, InvalidBillingDataError, CloudCostLinterError
except ImportError:
    # If run in standalone folder
    from .cloud_cost_linter import CloudCostLinter, InvalidBillingDataError, CloudCostLinterError

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB strict limit


def _safe_download_stem(filename: str) -> str:
    """Return a short, header-safe filename stem derived from an untrusted upload name."""
    if not isinstance(filename, str):
        filename = "uploaded_billing.csv"
    basename = os.path.basename(filename.replace("\\", "/"))
    stem, extension = os.path.splitext(basename)
    candidate = stem if extension.lower() == ".csv" else basename
    candidate = re.sub(r"[^A-Za-z0-9_-]+", "_", candidate).strip("_-")
    return (candidate[:80] or "uploaded_billing")


INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Cloud Cost Linter — Local Privacy-First Billing Analyzer</title>
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: #111827;
      --card-border: #1f2937;
      --card-hover: #1e293b;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --text-dim: #6b7280;
      --primary: #06b6d4;
      --primary-hover: #0891b2;
      --emerald: #10b981;
      --emerald-bg: rgba(16, 185, 129, 0.1);
      --amber: #f59e0b;
      --amber-bg: rgba(245, 158, 11, 0.1);
      --rose: #f43f5e;
      --rose-bg: rgba(244, 63, 94, 0.1);
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      line-height: 1.5;
      padding: 0;
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      background: rgba(17, 24, 39, 0.85);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 1rem 1.5rem;
    }
    .header-inner {
      max-width: 1200px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }
    .brand-badge {
      background: rgba(6, 182, 212, 0.15);
      border: 1px solid rgba(6, 182, 212, 0.3);
      color: #67e8f9;
      font-weight: 700;
      font-size: 0.85rem;
      padding: 0.3rem 0.6rem;
      border-radius: 6px;
      font-family: var(--font-mono);
    }
    .brand-title {
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }
    .status-badges {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.75rem;
      font-family: var(--font-mono);
    }
    .badge {
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }
    .badge-privacy {
      background: var(--emerald-bg);
      color: var(--emerald);
      border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .badge-budget {
      background: rgba(255, 255, 255, 0.05);
      color: #cbd5e1;
      border: 1px solid var(--card-border);
    }
    main {
      flex: 1;
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
      width: 100%;
    }
    .intro-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 2rem;
    }
    .intro-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.5rem;
      margin-top: 1rem;
    }
    .step-item {
      display: flex;
      gap: 0.75rem;
    }
    .step-number {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: var(--primary);
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 0.8rem;
      flex-shrink: 0;
    }
    .step-content h4 {
      font-size: 0.9rem;
      font-weight: 600;
      margin-bottom: 0.25rem;
    }
    .step-content p {
      font-size: 0.8rem;
      color: var(--text-muted);
    }
    .upload-container {
      background: var(--card-bg);
      border: 2px dashed var(--card-border);
      border-radius: 16px;
      padding: 2.5rem 1.5rem;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
      position: relative;
      margin-bottom: 2rem;
    }
    .upload-container:hover, .upload-container.dragover {
      border-color: var(--primary);
      background: var(--card-hover);
    }
    .upload-icon {
      font-size: 2.5rem;
      margin-bottom: 0.75rem;
    }
    .upload-title {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 0.35rem;
    }
    .upload-sub {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 1.25rem;
    }
    .upload-actions {
      display: flex;
      justify-content: center;
      gap: 1rem;
      flex-wrap: wrap;
    }
    .btn {
      padding: 0.6rem 1.25rem;
      border-radius: 8px;
      font-size: 0.875rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
    }
    .btn-primary {
      background: var(--primary);
      color: #fff;
    }
    .btn-primary:hover {
      background: var(--primary-hover);
    }
    .btn-secondary {
      background: #1f2937;
      color: #e5e7eb;
      border: 1px solid #374151;
    }
    .btn-secondary:hover {
      background: #374151;
    }
    .file-input {
      display: none;
    }
    .selected-file-chip {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(6, 182, 212, 0.1);
      border: 1px solid rgba(6, 182, 212, 0.3);
      padding: 0.35rem 0.75rem;
      border-radius: 9999px;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: #a5f3fc;
      margin-top: 1rem;
    }
    .alert-error {
      background: var(--rose-bg);
      border: 1px solid rgba(244, 63, 94, 0.3);
      color: #fecdd3;
      padding: 1rem 1.25rem;
      border-radius: 8px;
      margin-bottom: 1.5rem;
      font-size: 0.9rem;
      display: none;
    }
    .disclaimer-banner {
      background: rgba(245, 158, 11, 0.08);
      border: 1px solid rgba(245, 158, 11, 0.25);
      border-radius: 10px;
      padding: 1rem 1.25rem;
      margin-bottom: 1.5rem;
      font-size: 0.825rem;
      color: #fde68a;
      line-height: 1.5;
    }
    .disclaimer-banner strong {
      color: #fbbf24;
    }
    .results-container {
      display: none;
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    .kpi-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.25rem;
    }
    .kpi-label {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.35rem;
    }
    .kpi-value {
      font-size: 1.6rem;
      font-weight: 800;
      font-family: var(--font-mono);
      color: #fff;
    }
    .kpi-sub {
      font-size: 0.75rem;
      margin-top: 0.25rem;
    }
    .text-emerald { color: var(--emerald); }
    .text-amber { color: var(--amber); }
    .text-rose { color: var(--rose); }
    .panel {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 1.5rem;
    }
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid var(--card-border);
    }
    .panel-title {
      font-size: 1rem;
      font-weight: 700;
    }
    .service-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.75rem;
      font-size: 0.85rem;
    }
    .service-name {
      width: 180px;
      font-weight: 500;
    }
    .service-bar-container {
      flex: 1;
      height: 8px;
      background: #1f2937;
      border-radius: 4px;
      margin: 0 1rem;
      overflow: hidden;
    }
    .service-bar {
      height: 100%;
      background: var(--primary);
      border-radius: 4px;
    }
    .service-amount {
      width: 120px;
      text-align: right;
      font-family: var(--font-mono);
      font-weight: 600;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.825rem;
      text-align: left;
    }
    th {
      padding: 0.75rem 0.5rem;
      color: var(--text-muted);
      border-bottom: 1px solid var(--card-border);
      font-weight: 600;
    }
    td {
      padding: 0.75rem 0.5rem;
      border-bottom: 1px solid #1f2937;
    }
    .font-mono { font-family: var(--font-mono); }
    .tag-critical {
      background: var(--rose-bg);
      color: var(--rose);
      border: 1px solid rgba(244, 63, 94, 0.3);
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 700;
    }
    .tag-unconfirmed {
      background: var(--amber-bg);
      color: var(--amber);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 700;
    }
    .action-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
      margin-top: 2rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--card-border);
    }
    footer {
      border-top: 1px solid var(--card-border);
      padding: 1.5rem;
      text-align: center;
      font-size: 0.75rem;
      color: var(--text-dim);
      margin-top: auto;
    }
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <div class="brand">
        <span class="brand-badge">CCL-v2</span>
        <span class="brand-title">Cloud Cost Linter</span>
      </div>
      <div class="status-badges">
        <span class="badge badge-privacy">● 100% Local · Zero Telemetry</span>
        <span class="badge badge-budget">Zero-Budget Open Source</span>
      </div>
    </div>
  </header>

  <main>
    <!-- Non-technical instructions by Marketer -->
    <div class="intro-card">
      <h2 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.25rem;">Simple & Private Cloud Billing Audit</h2>
      <p style="font-size: 0.85rem; color: var(--text-muted);">
        Analyze your monthly cloud spending CSV without sharing data or using command lines. Your files never leave your computer.
      </p>
      <div class="intro-grid">
        <div class="step-item">
          <div class="step-number">1</div>
          <div class="step-content">
            <h4>Upload Billing CSV</h4>
            <p>Drag and drop your standard cloud billing CSV (GCP, AWS, Azure, or multi-cloud exports).</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-number">2</div>
          <div class="step-content">
            <h4>Review Anomaly Findings</h4>
            <p>Examine potential duplicate billing charges, high-cost outliers, and service distribution.</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-number">3</div>
          <div class="step-content">
            <h4>Download Reports</h4>
            <p>Export a clean, audit-ready CSV report or raw JSON for your FinOps / accounting review.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Banner -->
    <div id="errorBanner" class="alert-error"></div>

    <!-- Upload Zone -->
    <div class="upload-container" id="dropZone">
      <div class="upload-icon">📄</div>
      <div class="upload-title">Select or Drop Your Cloud Billing CSV</div>
      <div class="upload-sub">Strict local parsing · Max 10MB · Plain CSV format with (record_id, service, resource_id, date, cost)</div>
      <div class="upload-actions">
        <button type="button" class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
          Browse Local CSV
        </button>
        <button type="button" class="btn btn-secondary" id="sampleBtn">
          Load Sample Billing Data ($11.5k)
        </button>
      </div>
      <input type="file" id="fileInput" class="file-input" accept=".csv,text/csv">
      <div id="fileInfo" style="display: none;"></div>
    </div>

    <!-- Results Section -->
    <div id="resultsContainer" class="results-container">
      
      <!-- Inviolable Disclaimers Banner -->
      <div class="disclaimer-banner">
        <strong>Mandatory Accounting & Methodology Disclaimers:</strong><br>
        • <strong>Billing vs. State:</strong> Billing data alone CANNOT determine whether a resource is idle or active. Requires CloudWatch/Cloud Monitoring telemetry.<br>
        • <strong>Duplicates vs. Refunds:</strong> Potential duplicate charges are unconfirmed candidates for provider dispute, not guaranteed cash refunds.<br>
        • <strong>Rightsizing Projections:</strong> 40% rightsizing is an illustrative heuristic model. Verified realized savings remain <strong>$0.00</strong> until externally confirmed.
      </div>

      <!-- KPI Grid -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">Total Spend Audited</div>
          <div class="kpi-value" id="kpiSpend">$0.00</div>
          <div class="kpi-sub text-muted" id="kpiRecordCount">0 records</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Potential Duplicate Charges</div>
          <div class="kpi-value text-amber" id="kpiDuplicates">$0.00</div>
          <div class="kpi-sub text-amber" id="kpiDuplicateCount">0 items (unconfirmed)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Statistical Outliers</div>
          <div class="kpi-value text-rose" id="kpiAnomaliesCount">0</div>
          <div class="kpi-sub text-rose">Z-Score ≥ 2.0</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Total Estimated Savings</div>
          <div class="kpi-value text-emerald" id="kpiTotalSavings">$0.00</div>
          <div class="kpi-sub text-emerald">Illustrative Projection</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Verified Realized Savings</div>
          <div class="kpi-value" style="color: #94a3b8;">$0.00</div>
          <div class="kpi-sub text-muted">Verified Immediate Gain</div>
        </div>
      </div>

      <!-- Service Breakdown -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Spending by Service</div>
          <div style="font-size: 0.8rem; color: var(--text-muted);" id="topServiceLabel"></div>
        </div>
        <div id="serviceList"></div>
      </div>

      <!-- Potential Duplicates Table -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Potential Duplicate Charges (Subject to Provider Dispute)</div>
          <span class="tag-unconfirmed" id="dupBadge">0 candidate charges</span>
        </div>
        <div style="overflow-x: auto;">
          <table>
            <thead>
              <tr>
                <th>Duplicate ID</th>
                <th>Original ID</th>
                <th>Service</th>
                <th>Resource</th>
                <th>Date</th>
                <th>Cost</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="duplicatesTableBody"></tbody>
          </table>
        </div>
      </div>

      <!-- Cost Anomalies Table -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Statistically Expensive Outliers (Z-Score ≥ 2.0)</div>
          <span class="tag-critical" id="anomBadge">0 anomalies</span>
        </div>
        <div style="overflow-x: auto;">
          <table>
            <thead>
              <tr>
                <th>Severity</th>
                <th>Service</th>
                <th>Resource ID</th>
                <th>Cost</th>
                <th>Benchmark Mean</th>
                <th>Z-Score</th>
                <th>Telemetry Verification</th>
              </tr>
            </thead>
            <tbody id="anomaliesTableBody"></tbody>
          </table>
        </div>
      </div>

      <!-- Recommendations List -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Savings Recommendations & Heuristics</div>
          <span style="font-size: 0.75rem; color: var(--amber);">40% Illustrative Heuristic</span>
        </div>
        <div id="recommendationsList" style="display: flex; flex-direction: column; gap: 0.75rem;"></div>
      </div>

      <!-- Export Action Bar -->
      <div class="action-bar">
        <div style="font-size: 0.85rem; color: var(--text-muted);">
          Audited file: <span id="auditFileName" class="font-mono text-emerald"></span>
        </div>
        <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
          <button type="button" class="btn btn-secondary" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
            Analyze Another CSV
          </button>
          <button type="button" class="btn btn-secondary" id="downloadJsonBtn">
            Export JSON
          </button>
          <button type="button" class="btn btn-primary" id="downloadCsvBtn">
            Download CSV Analysis Report
          </button>
        </div>
      </div>

    </div>
  </main>

  <footer>
    Autonomous AI Society · Mission 002 Product Upgrade · Zero-Budget FinOps Engineering · 100% Offline & Private
  </footer>

  <script>
    let currentCsvText = null;
    let currentAnalysisData = null;
    let currentFileName = "sample_billing.csv";

    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');
    const errorBanner = document.getElementById('errorBanner');
    const resultsContainer = document.getElementById('resultsContainer');
    const sampleBtn = document.getElementById('sampleBtn');
    const downloadCsvBtn = document.getElementById('downloadCsvBtn');
    const downloadJsonBtn = document.getElementById('downloadJsonBtn');

    // Drag and drop handlers
    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
      }, false);
    });

    dropZone.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length) handleFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length) handleFile(e.target.files[0]);
    });

    sampleBtn.addEventListener('click', async (e) => {
      e.stopPropagation();
      try {
        hideError();
        const res = await fetch('/api/sample');
        if (!res.ok) throw new Error("Could not load sample file.");
        const text = await res.text();
        currentFileName = "sample_billing.csv";
        analyzeCsvContent(text, currentFileName);
      } catch (err) {
        showError("Failed to load sample billing data: " + err.message);
      }
    });

    function handleFile(file) {
      hideError();
      if (!file.name.toLowerCase().endsWith('.csv')) {
        showError("Invalid file type. Please upload a CSV file (.csv).");
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        showError("File size exceeds 10MB limit (" + (file.size / (1024*1024)).toFixed(1) + " MB).");
        return;
      }

      currentFileName = file.name;
      fileInfo.innerHTML = `<span class="selected-file-chip">✓ ${file.name} (${(file.size / 1024).toFixed(1)} KB)</span>`;
      fileInfo.style.display = 'block';

      const reader = new FileReader();
      reader.onload = (evt) => {
        analyzeCsvContent(evt.target.result, file.name);
      };
      reader.onerror = () => {
        showError("Failed to read local file.");
      };
      reader.readAsText(file);
    }

    async function analyzeCsvContent(csvText, fileName) {
      try {
        hideError();
        currentCsvText = csvText;
        const res = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ csv: csvText, filename: fileName })
        });

        const responseText = await res.text();
        let data = null;
        try {
          data = responseText ? JSON.parse(responseText) : null;
        } catch (parseError) {
          throw new Error(`Server returned an invalid response (HTTP ${res.status}). Please restart the local server and try again.`);
        }
        if (!data || typeof data !== 'object') {
          throw new Error(`Server returned an empty response (HTTP ${res.status}). Please restart the local server and try again.`);
        }
        if (!res.ok) {
          throw new Error(data.error || `Failed to analyze billing CSV (HTTP ${res.status}).`);
        }

        currentAnalysisData = data;
        renderResults(data);
      } catch (err) {
        showError(err.message);
        resultsContainer.style.display = 'none';
      }
    }

    function renderResults(data) {
      document.getElementById('auditFileName').textContent = data.file || currentFileName;
      document.getElementById('kpiSpend').textContent = '$' + data.summary.total_spending.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
      document.getElementById('kpiRecordCount').textContent = data.summary.record_count + ' records audited';

      document.getElementById('kpiDuplicates').textContent = '$' + data.potential_savings.potential_duplicate_charges.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
      document.getElementById('kpiDuplicateCount').textContent = data.summary.potential_duplicate_count + ' items (unconfirmed dispute)';

      document.getElementById('kpiAnomaliesCount').textContent = data.summary.expensive_anomalies_count;

      document.getElementById('kpiTotalSavings').textContent = '$' + (data.summary.illustrative_rightsizing_projection ?? 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});

      // Service Breakdown
      const srvList = document.getElementById('serviceList');
      srvList.innerHTML = '';
      const totalSpend = data.summary.total_spending;
      const sortedServices = Object.entries(data.spending_breakdown.spending_by_service);

      sortedServices.slice(0, 8).forEach(([srv, amt]) => {
        const pct = totalSpend > 0 ? (amt / totalSpend * 100) : 0;
        const row = document.createElement('div');
        row.className = 'service-row';
        row.innerHTML = `
          <div class="service-name">${escapeHtml(srv)}</div>
          <div class="service-bar-container">
            <div class="service-bar" style="width: ${Math.min(pct, 100)}%;"></div>
          </div>
          <div class="service-amount">$${amt.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} <span style="color: var(--text-dim); font-size: 0.75rem;">(${pct.toFixed(1)}%)</span></div>
        `;
        srvList.appendChild(row);
      });

      // Duplicates Table
      const dupBody = document.getElementById('duplicatesTableBody');
      dupBody.innerHTML = '';
      document.getElementById('dupBadge').textContent = `${data.duplicates.length} candidate charges`;
      if (data.duplicates.length === 0) {
        dupBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--emerald); padding: 1.5rem;">✓ No duplicate charges detected. Clean billing ledger.</td></tr>`;
      } else {
        data.duplicates.forEach(d => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td class="font-mono text-amber">${escapeHtml(d.duplicate_record_id)}</td>
            <td class="font-mono text-muted">${escapeHtml(d.original_record_id)}</td>
            <td>${escapeHtml(d.service)}</td>
            <td class="font-mono">${escapeHtml(d.resource_id)}</td>
            <td>${escapeHtml(d.date)}</td>
            <td class="font-mono font-bold">$${d.cost.toFixed(2)}</td>
            <td><span class="tag-unconfirmed">Unconfirmed Dispute</span></td>
          `;
          dupBody.appendChild(tr);
        });
      }

      // Anomalies Table
      const anomBody = document.getElementById('anomaliesTableBody');
      anomBody.innerHTML = '';
      document.getElementById('anomBadge').textContent = `${data.expensive_services.length} anomalies`;
      if (data.expensive_services.length === 0) {
        anomBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--emerald); padding: 1.5rem;">✓ No statistical cost outliers detected.</td></tr>`;
      } else {
        data.expensive_services.forEach(e => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><span class="${e.severity === 'CRITICAL' ? 'tag-critical' : 'tag-unconfirmed'}">${escapeHtml(e.severity)}</span></td>
            <td>${escapeHtml(e.service)}</td>
            <td class="font-mono">${escapeHtml(e.resource_id)}</td>
            <td class="font-mono font-bold">$${e.cost.toFixed(2)}</td>
            <td class="font-mono text-muted">$${e.mean_cost.toFixed(2)}</td>
            <td class="font-mono text-rose">${e.z_score.toFixed(2)}</td>
            <td style="font-size: 0.75rem; color: #fde68a;">Requires CPU/RAM telemetry audit (Billing != state)</td>
          `;
          anomBody.appendChild(tr);
        });
      }

      // Recommendations
      const recList = document.getElementById('recommendationsList');
      recList.innerHTML = '';
      data.potential_savings.recommendations.forEach(r => {
        const item = document.createElement('div');
        item.style.padding = '0.75rem 1rem';
        item.style.background = '#1e293b';
        item.style.borderRadius = '8px';
        item.style.display = 'flex';
        item.style.justifyContent = 'space-between';
        item.style.alignItems = 'flex-start';
        item.style.gap = '1rem';
        item.innerHTML = `
          <div>
            <div style="font-weight: 600; font-size: 0.85rem; margin-bottom: 0.25rem;">${escapeHtml(r.action)}</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Type: ${escapeHtml(r.type)} · Guaranteed: No</div>
          </div>
          <div style="font-family: var(--font-mono); font-weight: 700; color: var(--emerald); white-space: nowrap;">
            ~$${r.estimated_potential.toFixed(2)}
          </div>
        `;
        recList.appendChild(item);
      });

      resultsContainer.style.display = 'block';
      resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }

    // CSV Download
    downloadCsvBtn.addEventListener('click', async () => {
      if (!currentCsvText) return;
      try {
        const res = await fetch('/api/export-csv', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ csv: currentCsvText, filename: currentFileName })
        });
        if (!res.ok) throw new Error("Could not generate CSV report.");
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `cloud_cost_analysis_${currentFileName.replace(/\\.csv$/i, '')}.csv`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } catch (err) {
        showError("Failed to download CSV report: " + err.message);
      }
    });

    // JSON Download
    downloadJsonBtn.addEventListener('click', () => {
      if (!currentAnalysisData) return;
      const jsonStr = JSON.stringify(currentAnalysisData, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cloud_cost_analysis_${currentFileName.replace(/\\.csv$/i, '')}.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    });

    function showError(msg) {
      errorBanner.textContent = msg;
      errorBanner.style.display = 'block';
      errorBanner.scrollIntoView({ behavior: 'smooth' });
    }

    function hideError() {
      errorBanner.style.display = 'none';
      errorBanner.textContent = '';
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }
  </script>
</body>
</html>
"""


class CloudCostLinterHTTPHandler(BaseHTTPRequestHandler):
    """
    HTTP Request Handler serving the local web application and API endpoints.
    Uses pure Python standard library without third-party frameworks.
    """

    def _send_response_headers(self, status: int, content_type: str, content_length: Optional[int] = None, extra_headers: Optional[Dict[str, str]] = None):
        """Sends HTTP response headers with optional Content-Length and CORS headers."""
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        if content_length is not None:
            self.send_header("Content-Length", str(content_length))
        # Defense-in-depth headers for the local interface and API.
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'")
        # The interface is served from this same local origin; do not enable
        # cross-origin access to the local billing-analysis API.
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()

    def _set_headers(self, status: int = 200, content_type: str = "application/json"):
        """Send a response whose body is delimited by closing the connection."""
        self.close_connection = True
        self._send_response_headers(
            status,
            content_type,
            extra_headers={"Connection": "close"},
        )

    def do_OPTIONS(self):
        self._send_response_headers(200, "text/plain", content_length=0)

    def _handle_get_or_head(self, send_body: bool = True):
        """Handles GET and HEAD requests. HEAD sends identical headers without writing the body."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            body_bytes = INDEX_HTML.encode("utf-8")
            self._send_response_headers(200, "text/html; charset=utf-8", content_length=len(body_bytes))
            if send_body:
                self.wfile.write(body_bytes)
            return

        elif path == "/api/health":
            resp = {
                "status": "ok",
                "application": "Cloud Cost Linter",
                "version": "2.0.0",
                "privacy": "100% Local-First (No external network traffic)",
            }
            body_bytes = json.dumps(resp).encode("utf-8")
            self._send_response_headers(200, "application/json; charset=utf-8", content_length=len(body_bytes))
            if send_body:
                self.wfile.write(body_bytes)
            return

        elif path == "/api/sample":
            sample_path = os.path.join(os.path.dirname(__file__), "sample_billing.csv")
            if not os.path.exists(sample_path):
                sample_path = "sample_billing.csv"

            if os.path.exists(sample_path):
                with open(sample_path, "r", encoding="utf-8") as f:
                    content = f.read()
                body_bytes = content.encode("utf-8")
                self._send_response_headers(200, "text/csv; charset=utf-8", content_length=len(body_bytes))
                if send_body:
                    self.wfile.write(body_bytes)
            else:
                body_bytes = json.dumps({"error": "Sample billing file not found."}).encode("utf-8")
                self._send_response_headers(404, "application/json; charset=utf-8", content_length=len(body_bytes))
                if send_body:
                    self.wfile.write(body_bytes)
            return

        else:
            body_bytes = b"404 Not Found"
            self._send_response_headers(404, "text/plain; charset=utf-8", content_length=len(body_bytes))
            if send_body:
                self.wfile.write(body_bytes)

    def do_HEAD(self):
        """Processes HEAD request: returns all response headers identical to GET with zero body bytes."""
        self._handle_get_or_head(send_body=False)

    def do_GET(self):
        """Processes GET request: returns full response with headers and body."""
        self._handle_get_or_head(send_body=True)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. Validate Content-Length to prevent oversized denial of service
        content_length_header = self.headers.get("Content-Length")
        if not content_length_header:
            self._set_headers(400, "application/json; charset=utf-8")
            self.wfile.write(json.dumps({"error": "Missing Content-Length header."}).encode("utf-8"))
            return

        try:
            content_length = int(content_length_header)
        except ValueError:
            self._set_headers(400, "application/json; charset=utf-8")
            self.wfile.write(json.dumps({"error": "Invalid Content-Length header."}).encode("utf-8"))
            return

        if content_length < 0:
            self._set_headers(400, "application/json; charset=utf-8")
            self.wfile.write(json.dumps({"error": "Invalid negative Content-Length."}).encode("utf-8"))
            return

        if content_length > MAX_UPLOAD_SIZE:
            self._set_headers(413, "application/json; charset=utf-8")
            self.wfile.write(
                json.dumps({
                    "error": f"Payload Too Large: {content_length / (1024 * 1024):.1f} MB exceeds maximum allowed limit of {MAX_UPLOAD_SIZE // (1024 * 1024)} MB."
                }).encode("utf-8")
            )
            return

        body_bytes = self.rfile.read(content_length)

        # Parse payload (JSON or raw text)
        csv_text = ""
        filename = "uploaded_billing.csv"
        content_type = self.headers.get("Content-Type", "")

        try:
            if "application/json" in content_type:
                payload = json.loads(body_bytes.decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("JSON request body must be an object.")
                csv_text = payload.get("csv", "")
                if not isinstance(csv_text, str):
                    raise ValueError("CSV content must be a string.")
                supplied_filename = payload.get("filename", filename)
                filename = supplied_filename if isinstance(supplied_filename, str) else filename
            else:
                csv_text = body_bytes.decode("utf-8", errors="replace")
        except Exception as e:
            self._set_headers(400, "application/json; charset=utf-8")
            self.wfile.write(json.dumps({"error": f"Failed to parse request body: {e}"}).encode("utf-8"))
            return

        # Handle API Endpoints
        linter = CloudCostLinter()

        if path == "/api/analyze":
            try:
                results = linter.lint_content(csv_text, source_name=filename)
                self._set_headers(200, "application/json; charset=utf-8")
                self.wfile.write(json.dumps(results).encode("utf-8"))
            except CloudCostLinterError as err:
                self._set_headers(400, "application/json; charset=utf-8")
                self.wfile.write(json.dumps({"error": str(err)}).encode("utf-8"))
            except Exception as err:
                self._set_headers(500, "application/json; charset=utf-8")
                self.wfile.write(json.dumps({"error": "Analysis failed due to an internal server error."}).encode("utf-8"))

        elif path == "/api/export-csv":
            try:
                results = linter.lint_content(csv_text, source_name=filename)
                csv_report = linter.generate_csv_report(results)

                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", f'attachment; filename="cloud_cost_analysis_{_safe_download_stem(filename)}.csv"')
                self.end_headers()
                self.wfile.write(csv_report.encode("utf-8"))
            except CloudCostLinterError as err:
                self._set_headers(400, "application/json; charset=utf-8")
                self.wfile.write(json.dumps({"error": str(err)}).encode("utf-8"))
            except Exception as err:
                self._set_headers(500, "application/json; charset=utf-8")
                self.wfile.write(json.dumps({"error": "Export failed due to an internal server error."}).encode("utf-8"))

        elif path == "/api/export-json":
            try:
                results = linter.lint_content(csv_text, source_name=filename)
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Disposition", f'attachment; filename="cloud_cost_analysis_{_safe_download_stem(filename)}.json"')
                self.end_headers()
                self.wfile.write(json.dumps(results, indent=2).encode("utf-8"))
            except CloudCostLinterError as err:
                self._set_headers(400, "application/json; charset=utf-8")
                self.wfile.write(json.dumps({"error": str(err)}).encode("utf-8"))
            except Exception as err:
                self._set_headers(500, "application/json; charset=utf-8")
                self.wfile.write(json.dumps({"error": f"Export failed: {err}"}).encode("utf-8"))

        else:
            self._set_headers(404, "text/plain; charset=utf-8")
            self.wfile.write(b"404 Endpoint Not Found")

    def log_message(self, format, *args):
        # Override to keep terminal output clean during automated testing
        return


def run_web_server(port: int = 8080, host: str = "127.0.0.1"):
    """Launches local HTTP server on specified port and host interface."""
    server_address = (host, port)
    try:
        httpd = HTTPServer(server_address, CloudCostLinterHTTPHandler)
    except OSError as err:
        if err.errno == 98:  # Address already in use
            sys.stderr.write(
                f"\n[ERROR] Port {port} is already in use on {host}.\n"
                f"Please specify an alternate free port using --port <PORT> (e.g., --port 8085).\n\n"
            )
            sys.exit(1)
        raise err

    print("=" * 74)
    print("           CLOUD COST LINTER — LOCAL WEB INTERFACE (MISSION 002)")
    print("=" * 74)
    print(f" Status:       Running locally at http://{host}:{port}/")
    print(" Privacy:      100% Local-First. Zero telemetry, zero external APIs.")
    print(" Security:     Strict CSV validation · No execution of uploaded files.")
    print(" Dependencies: Python Standard Library Only (₹0 Development Budget)")
    print("-" * 74)
    print(" Press Ctrl+C to terminate.")
    print("=" * 74)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("\nLocal server terminated.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cloud Cost Linter Local Web Interface")
    parser.add_argument("positional_port", nargs="?", type=int, default=None, help="Port to listen on (optional positional argument)")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Port to listen on (default: 8080)")
    parser.add_argument("--host", "-H", type=str, default="127.0.0.1", help="Host interface to bind to (default: 127.0.0.1)")
    args = parser.parse_args()

    selected_port = args.positional_port if args.positional_port is not None else args.port
    run_web_server(port=selected_port, host=args.host)
