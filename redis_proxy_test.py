import unittest
from flask import Flask, jsonify
import redis
from cachetools import LRUCache
import time
import threading

from redis_proxy import app

class RedisProxyTest(unittest.TestCase):
    def setUp(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0) 
        self.app = app.test_client()
        self.concurrent_requests = 5

    def test_get_data(self):
        #set some test data
        self.redis_client.set('test_key', 'test_value')
        response = self.app.get('/get/test_key')
        self.assertEqual(response.status_code, 200)
        expected_data = {'key': 'test_key', 'value': 'test_value'}
        self.assertEqual(response.get_json(), expected_data)

    def test_get_data_key_not_found(self):
        response = self.app.get('/get/xxx')
        self.assertEqual(response.status_code, 404)
        expected_data = {'message': 'Key not found'}
        self.assertEqual(response.get_json(), expected_data)
    
    def test_cached_get(self):
        self.app.get('/set/key1/value1')
        response = self.app.get('/get/key1')
        self.assertEqual(response.status_code, 200)
        expected_data = {'key': 'key1', 'value': 'value1'}
        self.assertEqual(response.get_json(), expected_data)

    def test_cache_eviction(self): #tests LRU capability & fixed key size
        #for this test, make sure cache size has been configured to max_size = 2 in redis_proxy.py
        self.app.get('/set/key1/value1')
        self.app.get('/set/key2/value2')
        self.app.get('set/key3/value3')
        response = self.app.get('/get/key1')
        expected_data = {'message': 'Key not found'}
        self.assertEqual(response.get_json(), expected_data)
        response = self.app.get('/get/key3')
        expected_data_key3 = {'key': 'key3', 'value': 'value3'}
        self.assertEqual(response.get_json(), expected_data_key3)
    
    def test_global_expiry(self):
        self.app.get('/set/key4/value4')
        time.sleep(3)
        response = self.app.get('/get/key4')
        self.assertEqual(response.status_code, 404)
        expected_data = {'message': 'Key not found'}
        self.assertEqual(response.get_json(), expected_data)

    def test_sequential_concurrent_processing(self):  
        request_order = []
        def send_concurrent_requests():
            for i in range(self.concurrent_requests):
                response = self.app.get('/get/key')
                response_data = response.get_json()
                request_order.append(response_data['key'])
            threads = [threading.Thread(target=send_concurrent_requests) for _ in range(self.concurrent_requests)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            expected_order = [str(i) for i in range(self.concurrent_requests)]
            self.assertEqual(request_order, expected_order)
        

if __name__ == '__main__':
    unittest.main()
