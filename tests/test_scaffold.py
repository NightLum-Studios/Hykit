import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hykit.scaffold import create_project


class TestScaffold(unittest.TestCase):
    def test_existing_folder_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            existing = root / "MyMod"
            existing.mkdir()
            with self.assertRaises(FileExistsError):
                create_project("MyMod", "Author", destination_dir=root, template_path=root)

    def test_scaffold_with_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            template = root / "template"
            template.mkdir()
            file_path = template / "{PROJECT_NAME_PASCAL}.txt"
            file_path.write_text("Hello {PROJECT_NAME}", encoding="utf-8")

            target = create_project(
                "NightLumCore",
                "LandarHinofiori",
                destination_dir=root,
                template_path=template,
            )
            expected_file = target / "NightLumCore.txt"
            self.assertTrue(expected_file.exists())
            self.assertEqual(
                expected_file.read_text(encoding="utf-8"),
                "Hello NightLumCore",
            )

    def test_scaffold_without_author_uses_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            template = root / "template"
            template.mkdir()
            file_path = template / "manifest.txt"
            file_path.write_text("{PROJECT_AUTHOR}", encoding="utf-8")

            target = create_project(
                "NightLumCore",
                template_type="project",
                destination_dir=root,
                template_path=template,
            )
            self.assertEqual(
                (target / "manifest.txt").read_text(encoding="utf-8"),
                "hykit",
            )

    def test_scaffold_replaces_placeholders_in_kts_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            template = root / "template"
            template.mkdir()
            file_path = template / "settings.gradle.kts"
            file_path.write_text(
                'rootProject.name = "{PROJECT_NAME}"\nGroup = "{PROJECT_AUTHOR}"\n',
                encoding="utf-8",
            )

            target = create_project(
                "NightLumCore",
                "LandarHinofiori",
                template_type="project",
                destination_dir=root,
                template_path=template,
            )
            self.assertEqual(
                (target / "settings.gradle.kts").read_text(encoding="utf-8"),
                'rootProject.name = "NightLumCore"\nGroup = "LandarHinofiori"\n',
            )

    def test_failed_scaffold_does_not_leave_partial_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            template = root / "template"
            template.mkdir()
            (template / "README.md").write_text("content", encoding="utf-8")

            with patch("hykit.scaffold.rename_paths", side_effect=RuntimeError("boom")):
                with self.assertRaises(RuntimeError):
                    create_project(
                        "NightLumCore",
                        "LandarHinofiori",
                        template_type="project",
                        destination_dir=root,
                        template_path=template,
                    )

            self.assertFalse((root / "NightLumCore").exists())


if __name__ == "__main__":
    unittest.main()
