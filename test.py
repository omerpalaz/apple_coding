"""
Test file for apple_coding.py
Author: Omer Can Palaz
"""

import unittest
from apple_coding import FilesContainKeyword

class FilesContainKeywordTest(unittest.TestCase):
    """Tests for class FilesContainKeyword"""

    TEST_5_RESULT = {'test_dir-1': 0}
    TEST_6_RESULT = {'test_dir-2': 2}
    TEST_7_RESULT = {'test_dir-3': 2, 'test_dir-3/sub-1': 1, 'test_dir-3/sub-1/sub-1': 1, 'test_dir-3/sub-2': 1}
    TEST_8_RESULT = {'test_dir-4': 2}
    TEST_9_RESULT = {'test_dir-5': 1}
    TEST_10_RESULT = {'test_dir-6': 0, 'test_dir-6/sub-1': 1, 'test_dir-6/sub-2': 1}
    TEST_11_RESULT = {'test_dir-7': 1, 'test_dir-7/sub-1': 2}
    TEST_12_RESULT = {'test_dir-8': 1, 'test_dir-8/sub-1': 3, 'test_dir-8/sub-1/sub-2': 2}

    def test_1(self):
        """Raises ValueError if root_dir is None"""
        try:
            fck = FilesContainKeyword(None, "[a-zA-Z]+_TESTResult.*")
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)

    def test_2(self):
        """Raises ValueError if root_dir does NOT exist"""
        try:
            fck = FilesContainKeyword("test_dir", "[a-zA-Z]+_TESTResult.*")
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)

    def test_3(self):
        """Raises ValueError if keyword is None"""
        try:
            fck = FilesContainKeyword("test_dir-1", None)
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)

    def test_4(self):
        """Raises ValueError if keyword is NOT a valid regular expression"""
        try:
            fck = FilesContainKeyword("test_dir-1", "[a-zA-+_TESTResult.*")
            self.assertTrue(False)
        except ValueError as e:
            self.assertTrue(True)

    def test_5(self):
        """Tests test_dir-1 that has no file and no subdir"""
        fck = FilesContainKeyword("test_dir-1", "[a-zA-Z]+_TESTResult.*")
        result_count_dir = fck.walk_root_dir()
        self.assertDictEqual(result_count_dir, self.TEST_5_RESULT)

    def test_6(self):
        """Tests test_dir-2 that has just files"""
        fck = FilesContainKeyword("test_dir-2", "[a-zA-Z]+_TESTResult.*")
        result_count_dir = fck.walk_root_dir()
        self.assertDictEqual(result_count_dir, self.TEST_6_RESULT)

    def test_7(self):
        """Tests test_dir-3 that has subdirectories and files"""
        fck = FilesContainKeyword("test_dir-3", "[a-zA-Z]+_TESTResult.*")
        result_count_dir = fck.walk_root_dir()
        self.assertDictEqual(result_count_dir, self.TEST_7_RESULT)

    def test_8(self):
        """Tests test_dir-4 that has a file and a link to that file"""
        fck = FilesContainKeyword("test_dir-4", "[a-zA-Z]+_TESTResult.*")
        result_count_dir = fck.walk_root_dir()
        self.assertDictEqual(result_count_dir, self.TEST_8_RESULT)

    def test_9(self):
        """Tests test_dir-5 that has a file and a broken link"""
        fck = FilesContainKeyword("test_dir-5", "[a-zA-Z]+_TESTResult.*")
        result_count_dir = fck.walk_root_dir()
        self.assertDictEqual(result_count_dir, self.TEST_9_RESULT)

    def test_10(self):
        """Tests test_dir-6 that has a subdir and a link to that subdir"""
        fck = FilesContainKeyword("test_dir-6", "[a-zA-Z]+_TESTResult.*")
        result_count_dir = fck.walk_root_dir()
        self.assertDictEqual(result_count_dir, self.TEST_10_RESULT)

    def test_11(self):
        """Tests test_dir-7 that has a link to test_dir-7 (creates a loop)"""
        fck = FilesContainKeyword("test_dir-7", "[a-zA-Z]+_TESTResult.*")
        result_count_dir = fck.walk_root_dir()
        self.assertDictEqual(result_count_dir, self.TEST_11_RESULT)

    def test_12(self):
        """Tests test_dir-8 that has multiple level subdirectories. One subdir links to 2 level up dir (creates a loop between subdirs)"""
        fck = FilesContainKeyword("test_dir-8", "[a-zA-Z]+_TESTResult.*")
        result_count_dir = fck.walk_root_dir()
        self.assertDictEqual(result_count_dir, self.TEST_12_RESULT)

if __name__ == "__main__":
    unittest.main()