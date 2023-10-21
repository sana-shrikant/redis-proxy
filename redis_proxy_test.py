import unittest
from flask import Flask, jsonify
import redis
from cachetools import LRUCache
import time

from redis_proxy import app

class RedisProxyTest(unittest.TestCase):
    def setUp(self):
        #self.cache = LRUCache(maxsize=2) - unnecessary bc we are purely testing the cache through flask 
        #redis db should be set up for testing 
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0) #TODO: clarify bc im not 100% sure if needed
        #test client for the flask app
        self.app = app.test_client()

    def test_get_data(self):
        #set some test data
        self.redis_client.set('test_key', 'test_value')
        response = self.app.get('/get/test_key')
        #check if response is OK (200)
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
        #print(self.cache.get('key1'))
        #print(self.cache.currsize)
        response = self.app.get('/get/key1')
        # print(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        expected_data = {'key': 'key1', 'value': 'value1'}
        self.assertEqual(response.get_json(), expected_data)

    def test_cache_eviction(self): #tests LRU capability & fixed key size
        #for this test, make sure cache size has been configured to max_size = 2 in redis_proxy.py
        #question - should these values also be in the database? 
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


        


if __name__ == '__main__':
    unittest.main()
