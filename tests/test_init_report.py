import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/app-roast/scripts/init_report.py"


class InitReportTests(unittest.TestCase):
    def test_creates_report_with_lossless_quoted_metadata_and_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = 'Русский "target"\nstatus: complete {{tone_yaml}}'
            run = Path(temporary) / "run"
            result = subprocess.run([sys.executable, str(SCRIPT), "--target", target,
                                     "--output", str(run), "--language", "ru", "--tone", "brutal"],
                                    capture_output=True, text=True, check=True)
            report = run / "report.md"
            content = report.read_text()
            metadata = content.split("---", 2)[1]
            target_line = next(line for line in metadata.splitlines() if line.startswith("target: "))
            self.assertEqual(json.loads(target_line.removeprefix("target: ")), target)
            self.assertEqual(metadata.count("\nstatus:"), 1)
            self.assertIn("status: in-progress", metadata)
            self.assertTrue((run / "evidence").is_dir())
            self.assertEqual(result.stdout.strip(), str(report.resolve()))

    def test_refuses_to_overwrite_existing_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            report = Path(temporary) / "report.md"
            report.write_text("User findings must survive.\n")
            result = subprocess.run([sys.executable, str(SCRIPT), "--target", "app", "--output", temporary],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(report.read_text(), "User findings must survive.\n")

    def test_default_run_names_do_not_collide(self):
        with tempfile.TemporaryDirectory() as temporary:
            paths = [subprocess.run([sys.executable, str(SCRIPT), "--target", "app"],
                                    cwd=temporary, capture_output=True, text=True, check=True).stdout.strip()
                     for _ in range(2)]
            self.assertNotEqual(*paths)
            self.assertTrue(all(Path(path).is_file() for path in paths))


if __name__ == "__main__":
    unittest.main()
