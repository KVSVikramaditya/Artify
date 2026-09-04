import tempfile
import unittest
from pathlib import Path

from src.web import create_app


class ArtifyWebTests(unittest.TestCase):
    def test_homepage_loads(self):
        with tempfile.TemporaryDirectory() as runtime:
            app = create_app(Path(runtime))
            response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Make every moment", response.data)

    def test_empty_upload_is_rejected(self):
        with tempfile.TemporaryDirectory() as runtime:
            app = create_app(Path(runtime))
            response = app.test_client().post("/api/jobs", data={})
        self.assertEqual(response.status_code, 400)
