import unittest
from src.util import extract_title

class MyTestCase(unittest.TestCase):
    def test_extract_title(self):
        res = extract_title("# foo")
        self.assertEqual(res, "foo")  # add assertion here


    def test_extract_title_spaces(self):
        res = extract_title("  # foo   ")
        self.assertEqual(res, "foo")  # add assertion here


if __name__ == '__main__':
    unittest.main()
