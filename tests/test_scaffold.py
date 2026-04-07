import tempfile
import unittest
from pathlib import Path

from hykit.scaffold import create_project


class TestScaffold(unittest.TestCase):
    def test_existing_folder_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            existing = root / "MyMod"
            existing.mkdir()
            with self.assertRaises(FileExistsError):
                create_project("MyMod", destination_dir=root, template_path=root)

    def test_scaffold_with_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            template = root / "template"
            template.mkdir()
            file_path = template / "{PROJECT_NAME_PASCAL}.txt"
            file_path.write_text("Hello {PROJECT_NAME}", encoding="utf-8")

            target = create_project(
                "NightLumCore",
                destination_dir=root,
                template_path=template,
            )
            expected_file = target / "NightLumCore.txt"
            self.assertTrue(expected_file.exists())
            self.assertEqual(
                expected_file.read_text(encoding="utf-8"),
                "Hello NightLumCore",
            )


if __name__ == "__main__":
    unittest.main()
