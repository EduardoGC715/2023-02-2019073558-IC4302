import unittest
import controller

class TestBiorxiv(unittest.TestCase):
		
    response = None
    
    def setUp(self):
      response = controller.get_biorxiv_data()
      
    def testNoneResponse(self):
        self.assertIsNotNone(self.response, "The response is not supposed to be None")

    def tearDown(self):
        response = None

if __name__ == '__main__':
    unittest.main()