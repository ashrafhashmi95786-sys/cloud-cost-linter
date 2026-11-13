import unittest

from app import app

class RenderAppTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_health_and_security_headers(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
        self.assertIn("frame-ancestors 'none'", response.headers.get("Content-Security-Policy", ""))
        self.assertEqual(response.headers.get("Cache-Control"), "no-store")

    def test_hosted_privacy_notice_is_visible(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Hosted demo privacy notice", page)
        self.assertIn("transmitted to this server", page)
        self.assertNotIn("Your files never leave your computer", page)
        self.assertNotIn("100% Local · Zero Telemetry", page)

    def test_privacy_page_includes_future_advertising_disclosures(self):
        response = self.client.get("/privacy")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Advertising is not currently enabled", page)
        self.assertIn("prior visits to this website or other websites", page)
        self.assertIn("Google Ads Settings", page)
        self.assertIn("www.aboutads.info", page)
        self.assertIn("Google-certified consent management platform (CMP)", page)
        self.assertIn("IAB Europe Transparency and Consent Framework (TCF)", page)
        self.assertIn("https://support.google.com/adsense/answer/13554116", page)
        self.assertIn("This policy notice does not itself collect consent", page)

    def test_privacy_page_contact_uses_email_not_public_issue_tracker(self):
        response = self.client.get("/privacy")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn('mailto:ashwebtools95@gmail.com', page)
        self.assertNotIn('github.com/ashrafhashmi95786-sys/cloud-cost-linter/issues', page)

    def test_robots_txt_has_real_newlines_and_excludes_api(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.mimetype.startswith("text/plain"))
        body = response.get_data(as_text=True)
        self.assertIn("User-agent: *\n", body)
        self.assertIn("Allow: /\n", body)
        self.assertIn("Disallow: /api/\n", body)
        self.assertIn("Sitemap: https://cloud-cost-linter.onrender.com/sitemap.xml\n", body)
        self.assertNotIn("\\n", body)

    def test_hosted_privacy_notice_has_no_literal_newline_escape(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)
        self.assertIn("Do not upload confidential", page)
        self.assertNotIn("\\n    <!-- Upload Zone -->", page)

    def test_google_search_console_verification_file(self):
        response = self.client.get("/google2e731cb1546f4a5a.html")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/html")
        self.assertEqual(
            response.get_data(as_text=True),
            "google-site-verification: google2e731cb1546f4a5a.html",
        )


    def test_four_new_finops_guides_are_routed_and_in_sitemap(self):
        slugs = [
            "cloud-cost-allocation-tagging",
            "cloud-budget-forecast-variance",
            "cloud-data-transfer-costs",
            "cloud-commitment-discounts",
        ]
        for slug in slugs:
            response = self.client.get("/guides/" + slug)
            self.assertEqual(response.status_code, 200, slug)
            page = response.get_data(as_text=True)
            self.assertIn("<h1>", page)
            self.assertIn("Cloud Cost Linter", page)
        sitemap = self.client.get("/sitemap.xml").get_data(as_text=True)
        for slug in slugs:
            self.assertIn("/guides/" + slug, sitemap)


    def test_all_public_pages_and_guides_have_seo_metadata(self):
        page_slugs = ["privacy", "terms", "about", "contact"]
        guide_slugs = [
            "cloud-billing-csv-guide",
            "cloud-billing-anomaly-detection",
            "duplicate-cloud-billing-charges",
            "cloud-rightsizing-basics",
            "cloud-cost-allocation-tagging",
            "cloud-budget-forecast-variance",
            "cloud-data-transfer-costs",
            "cloud-commitment-discounts",
        ]
        for slug in page_slugs:
            response = self.client.get("/" + slug)
            self.assertEqual(response.status_code, 200, slug)
            page = response.get_data(as_text=True)
            self.assertIn("<title>", page, slug)
            self.assertIn('name="description"', page, slug)
            self.assertIn(
                f'<link rel="canonical" href="https://cloud-cost-linter.onrender.com/{slug}">',
                page,
                slug,
            )
            self.assertIn('name="robots" content="index,follow"', page, slug)

        for slug in guide_slugs:
            response = self.client.get("/guides/" + slug)
            self.assertEqual(response.status_code, 200, slug)
            page = response.get_data(as_text=True)
            self.assertIn("<title>", page, slug)
            self.assertIn('name="description"', page, slug)
            self.assertIn(
                f'<link rel="canonical" href="https://cloud-cost-linter.onrender.com/guides/{slug}">',
                page,
                slug,
            )
            self.assertIn('name="robots" content="index,follow"', page, slug)

    def test_guides_index_lists_all_eight_guides_and_has_seo_metadata(self):
        response = self.client.get("/guides")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.mimetype.startswith("text/html"))
        page = response.get_data(as_text=True)
        self.assertIn("<title>Cloud FinOps Guides and Tutorials | Cloud Cost Linter</title>", page)
        self.assertIn('name="description"', page)
        self.assertIn('rel="canonical" href="https://cloud-cost-linter.onrender.com/guides"', page)
        self.assertIn('name="robots" content="index,follow"', page)
        for slug in [
            "cloud-billing-csv-guide",
            "cloud-billing-anomaly-detection",
            "duplicate-cloud-billing-charges",
            "cloud-rightsizing-basics",
            "cloud-cost-allocation-tagging",
            "cloud-budget-forecast-variance",
            "cloud-data-transfer-costs",
            "cloud-commitment-discounts",
        ]:
            self.assertIn(f'href="/guides/{slug}"', page)

    def test_sitemap_contains_all_14_unique_public_urls(self):
        import xml.etree.ElementTree as ET

        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        root = ET.fromstring(response.get_data(as_text=True))
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [
            node.text
            for node in root.findall("sm:url/sm:loc", namespace)
        ]
        self.assertEqual(len(urls), 14)
        self.assertEqual(len(set(urls)), 13)
        self.assertIn("https://cloud-cost-linter.onrender.com/", urls)\n        self.assertIn("https://cloud-cost-linter.onrender.com/guides", urls)

    def test_sample_endpoint(self):
        response = self.client.get("/api/sample")
        self.assertEqual(response.status_code, 200)
        self.assertIn("record_id,service,resource_id,date,cost", response.get_data(as_text=True))

    def test_analyze_sample_csv(self):
        sample = self.client.get("/api/sample").get_data(as_text=True)
        response = self.client.post("/api/analyze", json={"csv": sample, "filename": "sample_billing.csv"})
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertIn("summary", result)
        self.assertAlmostEqual(result["summary"]["total_spending"], 11575.75)

    def test_reject_non_json_and_invalid_payload(self):
        self.assertEqual(self.client.post("/api/analyze", data="nope").status_code, 400)
        self.assertEqual(self.client.post("/api/analyze", json={"csv": 123}).status_code, 400)

    def test_export_csv_and_json(self):
        sample = self.client.get("/api/sample").get_data(as_text=True)
        payload = {"csv": sample, "filename": "sample_billing.csv"}
        csv_response = self.client.post("/api/export-csv", json=payload)
        json_response = self.client.post("/api/export-json", json=payload)
        self.assertEqual(csv_response.status_code, 200)
        self.assertIn("attachment;", csv_response.headers.get("Content-Disposition", ""))
        self.assertEqual(json_response.status_code, 200)
        self.assertIn("summary", json_response.get_json())

if __name__ == "__main__":
    unittest.main()
