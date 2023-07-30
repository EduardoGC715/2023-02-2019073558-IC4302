import unittest
from methods import *

class TestStringMethods(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(hello(), 'world1')

if __name__ == '__main__':
    unittest.main()