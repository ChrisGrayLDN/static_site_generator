import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# Hello")

        self.assertEqual("Hello", title)

    def test_extract_title_with_extra_hash(self):
        title = extract_title("# #Hello")

        self.assertEqual("#Hello", title)
