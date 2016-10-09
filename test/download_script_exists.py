import os
import unittest


class TumblyCLExists(unittest.TestCase):

    def test_file(self):
        file = os.path.isfile('tumbly/download.py')
        self.assertTrue(file)


if __name__ == '__main__':
    unittest.main()
