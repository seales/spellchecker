
import unittest

import common.utils as utils

# TODO - add more tests

class TestUtilsMethods(unittest.TestCase):

    def test_strip_string(self):
        self.assertEqual(utils.strip_string("^&#*#*#*#   foo   &#&#&#&#&#").strip(" "), "foo")

    def test_consolidate_spelling_errors(self):
        pass

    def test_spelling_group_list_from_hash(self):
        pass

    def test_split_line(self):
        pass

    def test_convert(self):
        pass

    def test_update_file(self):
        pass

    def test_remove_non_utf8(self):
        pass

    def test_is_two_part_word(self):
        self.assertTrue(utils.is_two_part_word("twopart"))
        self.assertTrue(utils.is_two_part_word("morewords"))
        self.assertFalse(utils.is_two_part_word("word"))

    def test_is_spelling_error(self):
        self.assertFalse(utils.is_spelling_error("word"))
        self.assertTrue(utils.is_spelling_error("wo23io234as;dfjd"))

if __name__ == '__main__':
    unittest.main()

