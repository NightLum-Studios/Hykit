import unittest

from hykit.placeholders import (
    DEFAULT_PROJECT_AUTHOR,
    build_placeholders,
    build_project_name,
    normalize_author_name,
    replace_placeholders,
)


class TestPlaceholders(unittest.TestCase):
    def test_build_placeholders(self) -> None:
        placeholders = build_placeholders("NightLumCore", "LandarHinofiori")
        self.assertEqual(placeholders["{PROJECT_NAME}"], "NightLumCore")
        self.assertEqual(placeholders["{PROJECT_NAME_LOWER}"], "nightlumcore")
        self.assertEqual(placeholders["{PROJECT_NAME_SNAKE}"], "night_lum_core")
        self.assertEqual(placeholders["{PROJECT_NAME_KEBAB}"], "night-lum-core")
        self.assertEqual(placeholders["{PROJECT_NAME_PASCAL}"], "NightLumCore")
        self.assertEqual(placeholders["{PROJECT_NAME_UPPER}"], "NIGHTLUMCORE")
        self.assertEqual(placeholders["{PROJECT_AUTHOR}"], "LandarHinofiori")

    def test_replace_placeholders(self) -> None:
        mapping = build_placeholders("MyMod", "Author")
        text = "Name: {PROJECT_NAME_PASCAL} by {PROJECT_AUTHOR}"
        self.assertEqual(replace_placeholders(text, mapping), "Name: MyMod by Author")

    def test_missing_author_uses_default(self) -> None:
        mapping = build_placeholders("MyMod", None)
        self.assertEqual(mapping["{PROJECT_AUTHOR}"], DEFAULT_PROJECT_AUTHOR)

    def test_invalid_name(self) -> None:
        with self.assertRaises(ValueError):
            build_project_name("   ")

    def test_invalid_project_names_are_rejected(self) -> None:
        for value in ("../bad", "bad/name", "bad\\name", "bad:name", "CON", "bad."):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    build_project_name(value)

    def test_invalid_author_name_is_rejected(self) -> None:
        for value in ('Bad"Author', "Bad\nAuthor", "Bad/Author"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    normalize_author_name(value)


if __name__ == "__main__":
    unittest.main()
