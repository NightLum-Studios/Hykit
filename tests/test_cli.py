import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from hykit.analyzer.issues import Issue
from hykit.cli import main


class TestCli(unittest.TestCase):
    def test_create_runs_validation_after_scaffolding(self) -> None:
        stdout = io.StringIO()
        with (
            patch("hykit.cli.create_project", return_value=Path("C:/tmp/MyMod")) as create_mock,
            patch("hykit.cli.validate_path", return_value=[]) as validate_mock,
            redirect_stdout(stdout),
        ):
            exit_code = main(["create", "project", "MyMod", "Author"])

        self.assertEqual(exit_code, 0)
        create_mock.assert_called_once()
        validate_mock.assert_called_once_with(Path("C:/tmp/MyMod"))
        output = stdout.getvalue()
        self.assertIn("Project created at C:\\tmp\\MyMod", output)
        self.assertIn("Validation completed successfully.", output)

    def test_create_returns_error_when_post_validation_fails(self) -> None:
        stdout = io.StringIO()
        issues = [
            Issue(
                severity="error",
                code="MANIFEST_MISSING",
                message="manifest.json was not found in the expected project locations.",
                file=Path("C:/tmp/MyMod/manifest.json"),
            )
        ]
        with (
            patch("hykit.cli.create_project", return_value=Path("C:/tmp/MyMod")),
            patch("hykit.cli.validate_path", return_value=issues),
            redirect_stdout(stdout),
        ):
            exit_code = main(["create", "project", "MyMod", "Author"])

        self.assertEqual(exit_code, 1)
        self.assertIn("MANIFEST_MISSING", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
