"""Check CI installer phases without changing host dependencies."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CiInstallerTests(unittest.TestCase):
    def run_installer(self, **variables):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / "calls"
            for name in ("sudo", "python"):
                command = root / name
                command.write_text(
                    f'#!/bin/sh\nprintf "%s\\n" "{name} $*" >> "$CALLS"\n'
                    f'[ "${{FAIL_MATCH:-}}" != "{name} $*" ] || exit 17\n'
                )
                command.chmod(0o755)
            env = os.environ.copy()
            env.pop("CI_SYSTEM_DEPS_ONLY", None)
            env.pop("CI_SYSTEM_DEPS_READY", None)
            env.update(
                PATH=f"{root}:{env['PATH']}",
                CALLS=str(log),
                DJANGO_VERSION="django~=6.0.0",
                **variables,
            )
            result = subprocess.run(
                [str(ROOT / "install-ci-deps.sh")],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            return result, log.read_text().splitlines()

    def test_phase_selection_and_failure(self):
        for variables, expected, status in (
            ({"CI_SYSTEM_DEPS_ONLY": "1"}, ["sudo npm install -g prettier"], 0),
            (
                {"CI_SYSTEM_DEPS_READY": "1"},
                [
                    "python -m pip install -U pip wheel setuptools",
                    "python -m pip install -U -e .[test]",
                    "python -m pip install -U django~=6.0.0",
                ],
                0,
            ),
            (
                {},
                [
                    "sudo npm install -g prettier",
                    "python -m pip install -U pip wheel setuptools",
                    "python -m pip install -U -e .[test]",
                    "python -m pip install -U django~=6.0.0",
                ],
                0,
            ),
            (
                {"FAIL_MATCH": "sudo npm install -g prettier"},
                ["sudo npm install -g prettier"],
                17,
            ),
        ):
            with self.subTest(variables=variables):
                result, calls = self.run_installer(**variables)
                self.assertEqual(result.returncode, status, result.stderr)
                self.assertEqual(calls, expected)
