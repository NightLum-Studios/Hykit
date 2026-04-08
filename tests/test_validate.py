import json
import tempfile
import unittest
from pathlib import Path

from hykit.analyzer import validate_path


class TestValidate(unittest.TestCase):
    def _minimal_manifest(self) -> dict[str, object]:
        return {
            "Group": "Author",
            "Name": "Project",
            "Version": "1.0.0",
            "Description": "",
            "Authors": [
                {
                    "Name": "Author",
                    "Email": "",
                    "Url": "",
                }
            ],
            "Website": "",
            "DisabledByDefault": False,
            "IncludesAssetPack": False,
            "Dependencies": {},
            "OptionalDependencies": {},
            "ServerVersion": "*",
            "Main": "dev.project.ExamplePlugin",
        }

    def _write_valid_project(self, root: Path, nested: bool = False) -> Path:
        module_root = root / "MyPlugin" if nested else root
        resources = module_root / "src" / "main" / "resources"
        java_dir = module_root / "src" / "main" / "java" / "dev" / "project"
        wrapper_dir = module_root / "gradle" / "wrapper"

        resources.mkdir(parents=True, exist_ok=True)
        java_dir.mkdir(parents=True, exist_ok=True)
        wrapper_dir.mkdir(parents=True, exist_ok=True)

        (resources / "manifest.json").write_text(
            json.dumps(self._minimal_manifest()),
            encoding="utf-8",
        )
        (java_dir / "ExamplePlugin.java").write_text(
            "package dev.project;\n\npublic class ExamplePlugin {\n}\n",
            encoding="utf-8",
        )
        (module_root / "build.gradle").write_text("plugins {}\n", encoding="utf-8")
        (module_root / "settings.gradle").write_text(
            'rootProject.name = "Project"\n',
            encoding="utf-8",
        )
        (module_root / "gradlew").write_text("", encoding="utf-8")
        (module_root / "gradlew.bat").write_text("", encoding="utf-8")
        (wrapper_dir / "gradle-wrapper.properties").write_text("", encoding="utf-8")
        return module_root

    def _write_valid_kts_project(self, root: Path) -> Path:
        module_root = self._write_valid_project(root)
        (module_root / "build.gradle").unlink()
        (module_root / "settings.gradle").unlink()
        (module_root / "build.gradle.kts").write_text("plugins {}\n", encoding="utf-8")
        (module_root / "settings.gradle.kts").write_text(
            'rootProject.name = "Project"\n',
            encoding="utf-8",
        )
        return module_root

    def test_manifest_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            issues = validate_path(Path(temp_dir))
            codes = {issue.code for issue in issues}
            self.assertIn("MANIFEST_MISSING", codes)

    def test_manifest_invalid_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "manifest.json").write_text("{", encoding="utf-8")
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MANIFEST_INVALID_JSON", codes)

    def test_manifest_found_in_resources_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root, nested=True)
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertNotIn("MANIFEST_MISSING", codes)
            self.assertEqual(issues, [])

    def test_missing_includes_asset_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "manifest.json").write_text(
                json.dumps({"Name": "Example"}), encoding="utf-8"
            )
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MANIFEST_MISSING_ASSET_PACK", codes)

    def test_invalid_json_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            (root / "data.json").write_text("{", encoding="utf-8")
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("JSON_INVALID", codes)

    def test_missing_required_manifest_field(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            manifest = self._minimal_manifest()
            del manifest["ServerVersion"]
            (root / "src" / "main" / "resources" / "manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MANIFEST_MISSING_FIELD", codes)

    def test_successful_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            issues = validate_path(root)
            self.assertEqual(issues, [])

    def test_manifest_with_utf8_bom_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            (root / "src" / "main" / "resources" / "manifest.json").write_text(
                json.dumps(self._minimal_manifest()),
                encoding="utf-8-sig",
            )
            issues = validate_path(root)
            self.assertEqual(issues, [])

    def test_manifest_main_missing_when_field_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            manifest = self._minimal_manifest()
            del manifest["Main"]
            (root / "src" / "main" / "resources" / "manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MANIFEST_MAIN_MISSING", codes)

    def test_manifest_main_missing_when_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            manifest = self._minimal_manifest()
            manifest["Main"] = "   "
            (root / "src" / "main" / "resources" / "manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MANIFEST_MAIN_MISSING", codes)

    def test_manifest_main_missing_when_not_string(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            manifest = self._minimal_manifest()
            manifest["Main"] = 123
            (root / "src" / "main" / "resources" / "manifest.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MANIFEST_MAIN_MISSING", codes)

    def test_main_class_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            (root / "src" / "main" / "java" / "dev" / "project" / "ExamplePlugin.java").unlink()
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MAIN_CLASS_MISSING", codes)

    def test_main_class_package_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            (root / "src" / "main" / "java" / "dev" / "project" / "ExamplePlugin.java").write_text(
                "package dev.other;\n\npublic class WrongPlugin {\n}\n",
                encoding="utf-8",
            )
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("MAIN_CLASS_PACKAGE_MISMATCH", codes)

    def test_java_package_placeholder_leak(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            (root / "README.md").write_text("{PROJECT_NAME}\n", encoding="utf-8")
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("JAVA_PACKAGE_PLACEHOLDER_LEAK", codes)

    def test_build_files_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            (root / "build.gradle").unlink()
            (root / "settings.gradle").unlink()
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("BUILD_FILES_MISSING", codes)

    def test_build_files_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertNotIn("BUILD_FILES_MISSING", codes)

    def test_build_kts_files_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_kts_project(root)
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertNotIn("BUILD_FILES_MISSING", codes)

    def test_build_files_missing_for_mixed_gradle_pair(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            (root / "settings.gradle").unlink()
            (root / "settings.gradle.kts").write_text(
                'rootProject.name = "Project"\n',
                encoding="utf-8",
            )
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("BUILD_FILES_MISSING", codes)

    def test_gradle_wrapper_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            (root / "gradlew").unlink()
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertIn("GRADLE_WRAPPER_MISSING", codes)

    def test_gradle_wrapper_present(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)
            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertNotIn("GRADLE_WRAPPER_MISSING", codes)

    def test_validate_ignores_tooling_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_valid_project(root)

            ignored_build = root / "build"
            ignored_build.mkdir()
            (ignored_build / "broken.json").write_text("{", encoding="utf-8")

            ignored_git = root / ".git"
            ignored_git.mkdir()
            (ignored_git / "README.md").write_text("{PROJECT_NAME}", encoding="utf-8")

            ignored_node_modules = root / "node_modules"
            ignored_node_modules.mkdir()
            (ignored_node_modules / "data.json").write_text("{", encoding="utf-8")

            issues = validate_path(root)
            codes = {issue.code for issue in issues}
            self.assertEqual(issues, [])
            self.assertNotIn("JSON_INVALID", codes)
            self.assertNotIn("JAVA_PACKAGE_PLACEHOLDER_LEAK", codes)


if __name__ == "__main__":
    unittest.main()
