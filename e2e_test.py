import unittest
import requests
import time
import redis

class EndToEndTest(unittest.TestCase):
    def test_get_data(self):
        url = "http://localhost:5000/get/test_key"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        expected_data = {'key': 'test_key', 'value': 'test_value'}
        self.assertEqual(response.json(), expected_data)
    def test_get_data_key_not_found(self):
        # URL for a non-existent key

        url = "http://localhost:5000/get/nonexistent_key"
        # Send an HTTP GET request to the proxy
        response = requests.get(url)

        # Verify that the response indicates the key was not found (status code 404)
        self.assertEqual(response.status_code, 404)
        expected_data = {'message': 'Key not found'}
        self.assertEqual(response.json(), expected_data)
    

if __name__ == '__main__':
    unittest.main()
