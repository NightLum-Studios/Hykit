import unittest
from pathlib import Path

from hykit.analyzer.issues import Issue
from hykit.analyzer.reporter import Reporter


class TestReporter(unittest.TestCase):
    def test_render_without_color(self) -> None:
        reporter = Reporter(root_path=Path("C:/project"), enable_color=False)
        output = reporter.render([])
        self.assertEqual(output, "Validation completed successfully.")

    def test_render_with_color(self) -> None:
        reporter = Reporter(root_path=Path("C:/project"), enable_color=True)
        issues = [
            Issue(
                severity="error",
                code="MANIFEST_MISSING",
                message="manifest.json was not found in the project root.",
                file=Path("C:/project/manifest.json"),
            )
        ]
        output = reporter.render(issues)
        self.assertIn("\033[31m[ERROR] MANIFEST_MISSING\033[0m", output)
        self.assertIn("\033[31mValidation completed: 1 errors, 0 warnings.\033[0m", output)


if __name__ == "__main__":
    unittest.main()
