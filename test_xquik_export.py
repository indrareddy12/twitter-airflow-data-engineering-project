import tempfile
import unittest
from pathlib import Path

from xquik_export import load_xquik_rows


class XquikExportTests(unittest.TestCase):
    def test_loads_json_export(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "tweets.json"
            path.write_text('{"tweets":[{"text":"Hello","like_count":3}]}', encoding="utf-8")

            rows = load_xquik_rows(path)

        self.assertEqual(rows[0]["text"], "Hello")
        self.assertEqual(rows[0]["favorite_count"], 3)

    def test_loads_csv_export(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "tweets.csv"
            path.write_text("full_text,username\nPipeline ready,dev\n", encoding="utf-8")

            rows = load_xquik_rows(path)

        self.assertEqual(rows[0]["user"], "dev")
        self.assertEqual(rows[0]["text"], "Pipeline ready")

    def test_rejects_missing_text(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "tweets.json"
            path.write_text('[{"id":"1"}]', encoding="utf-8")

            with self.assertRaises(ValueError):
                load_xquik_rows(path)


if __name__ == "__main__":
    unittest.main()
