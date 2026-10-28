from contextlib import contextmanager
import errno
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


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
            expected_root = (Path(temporary) / ".agents" / "app-grill").resolve()
            self.assertTrue(all(Path(path).parent.parent == expected_root for path in paths))

    def test_evidence_file_conflict_leaves_no_report_and_can_be_retried(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            evidence = output / "evidence"
            evidence.write_text("Existing user material.\n")
            command = [sys.executable, str(SCRIPT), "--target", "app", "--output", temporary]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(evidence.read_text(), "Existing user material.\n")
            self.assertFalse((output / "report.md").exists())
            evidence.unlink()
            subprocess.run(command, capture_output=True, text=True, check=True)
            self.assertTrue((output / "report.md").is_file())
            self.assertEqual(list(evidence.iterdir()), [])

    def test_unwritable_evidence_fails_before_creating_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            evidence = output / "evidence"
            evidence.mkdir()
            evidence.chmod(0o500)
            try:
                try:
                    with tempfile.TemporaryFile(dir=evidence):
                        pass
                except PermissionError:
                    pass
                else:
                    self.skipTest("This process can write to a read-only directory")
                command = [sys.executable, str(SCRIPT), "--target", "app", "--output", temporary]
                result = subprocess.run(command, capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse((output / "report.md").exists())
                self.assertEqual(list(evidence.iterdir()), [])
            finally:
                evidence.chmod(0o700)
            subprocess.run(command, capture_output=True, text=True, check=True)
            self.assertTrue((output / "report.md").is_file())

    def test_failed_report_write_removes_only_its_partial_report(self):
        spec = importlib.util.spec_from_file_location("app_roast_initializer", SCRIPT)
        initializer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(initializer)
        original_open = Path.open
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            report = output / "report.md"
            existing = output / "keep.txt"
            existing.write_text("Existing user material.\n")

            @contextmanager
            def failing_open(path, mode="r", *args, **kwargs):
                with original_open(path, mode, *args, **kwargs) as handle:
                    if path == report and mode == "x":
                        class DiskFullWriter:
                            def write(self, text):
                                handle.write(text[:12])
                                handle.flush()
                                raise OSError(errno.ENOSPC, "Simulated disk full")
                        yield DiskFullWriter()
                    else:
                        yield handle

            errors = io.StringIO()
            argv = [str(SCRIPT), "--target", "app", "--output", temporary]
            with mock.patch.object(Path, "open", failing_open), mock.patch.object(sys, "argv", argv), mock.patch("sys.stderr", errors):
                with self.assertRaises(SystemExit) as stopped:
                    initializer.main()
            self.assertEqual(stopped.exception.code, 1)
            self.assertIn("Simulated disk full", errors.getvalue())
            self.assertFalse(report.exists())
            self.assertEqual(existing.read_text(), "Existing user material.\n")
            subprocess.run([sys.executable, *argv], capture_output=True, text=True, check=True)
            self.assertTrue(report.is_file())


if __name__ == "__main__":
    unittest.main()
