import unittest

from hykit.placeholders import build_placeholders, build_project_name, replace_placeholders


class TestPlaceholders(unittest.TestCase):
    def test_build_placeholders(self) -> None:
        placeholders = build_placeholders("NightLumCore")
        self.assertEqual(placeholders["{PROJECT_NAME}"], "NightLumCore")
        self.assertEqual(placeholders["{PROJECT_NAME_LOWER}"], "nightlumcore")
        self.assertEqual(placeholders["{PROJECT_NAME_SNAKE}"], "night_lum_core")
        self.assertEqual(placeholders["{PROJECT_NAME_KEBAB}"], "night-lum-core")
        self.assertEqual(placeholders["{PROJECT_NAME_PASCAL}"], "NightLumCore")
        self.assertEqual(placeholders["{PROJECT_NAME_UPPER}"], "NIGHTLUMCORE")

    def test_replace_placeholders(self) -> None:
        mapping = build_placeholders("MyMod")
        text = "Name: {PROJECT_NAME_PASCAL}"
        self.assertEqual(replace_placeholders(text, mapping), "Name: MyMod")

    def test_invalid_name(self) -> None:
        with self.assertRaises(ValueError):
            build_project_name("   ")


if __name__ == "__main__":
    unittest.main()
