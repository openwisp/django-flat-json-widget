"""Check focused test selection and argument validation."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CiEntrypointTests(unittest.TestCase):
    def test_rejects_unsupported_arguments(self):
        for argument in (
            "--settings=other",
            "os.system",
            "flat_json_widget.tests.Helper.test_run",
        ):
            with self.subTest(argument=argument):
                result = subprocess.run(
                    [sys.executable, str(ROOT / "runtests"), argument],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertIn("unsupported", result.stderr.lower())

    def test_runs_a_focused_widget_test(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "runtests"),
                "flat_json_widget.tests.TestFlatJsonWidget.test_media",
                "--noinput",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ran 1 test", result.stderr)

    def test_default_dispatches_in_process(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copy2(ROOT / "runtests", root / "runtests")
            (root / "tests").mkdir()
            (root / "django" / "core").mkdir(parents=True)
            (root / "django" / "__init__.py").write_text("def setup(): pass\n")
            (root / "django" / "core" / "__init__.py").touch()
            (root / "django" / "core" / "management.py").write_text(
                "def execute_from_command_line(args): print('|'.join(args[1:]))\n"
            )
            result = subprocess.run(
                [sys.executable, str(root / "runtests")],
                cwd=root,
                env={**os.environ, "PYTHONPATH": str(root)},
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "test|flat_json_widget|tests")
