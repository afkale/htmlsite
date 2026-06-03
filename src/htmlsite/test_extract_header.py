import unittest

from htmlsite import extract_title


class TestExtractHeader(unittest.TestCase):
    def test_extract_header(self):
        result = extract_title("""# This is the header
this not
#this neither
 # this is not a header too
                """)
        self.assertEqual("This is the header", result)

    def test_extract_header_empty(self):
        result = extract_title("""""")
        self.assertEqual("", result)

    def test_extract_header_not_at_first_line(self):
        result = extract_title("""somerandomeshit
# header
                                """)
        self.assertEqual("header", result)
