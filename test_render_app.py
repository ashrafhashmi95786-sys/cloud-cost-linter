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
