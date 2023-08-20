import unittest
import crawler

class TestBiorxiv(unittest.TestCase):
		
    response = None
    
    def setUp(self):
      response = crawler.get_biorxiv_data()
      
    def testNoneResponse(self):
        self.assertIsNone(self.response, "The response is not supposed to be None")

    def tearDown(self):
        response = None

if __name__ == '__main__':
    unittest.main()