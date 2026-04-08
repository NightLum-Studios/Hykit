import unittest
from importlib.metadata import version

import hykit


class TestMetadata(unittest.TestCase):
    def test_package_version_matches_metadata(self) -> None:
        self.assertEqual(hykit.__version__, version("hykit"))


if __name__ == "__main__":
    unittest.main()
