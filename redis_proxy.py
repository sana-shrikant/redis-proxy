from flask import Flask, request, jsonify
import redis 
from cachetools import LRUCache
from cachetools import TTLCache
from datetime import datetime

app = Flask(__name__)

cache_max_size = 2 #TODO: figure out what this number should be - rn it's arbitrarily 1000  (testing purposes = 2)
global_expiry_seconds = 2 #TODO: figure out what this should be - rn 1  hour (testing purposes = 2)

redis_client = redis.StrictRedis(host = 'localhost', port=6379, db=0)
#cache = LRUCache(maxsize = 2) 
cache = TTLCache(maxsize = cache_max_size, ttl = global_expiry_seconds)
@app.route('/set/<key>/<value>', methods=['GET'])
#this is primarily for testing purposes
def set_data(key, value):
    cache[key] = value
    return ('', 204)
@app.route('/get/<key>', methods= ['GET'])
def get_data(key):
    #check the cache first
    cached_value = cache.get(key)
    if cached_value is not None:
        return jsonify({'key': key, 'value': cached_value})
    #val not in cache - look in redis db 
    value = redis_client.get(key)
    if value:
        #if len(cache) >= cache.maxsize:
            #remove LRU item to make room for new one 
        #    cache.popitem()
        cache[key] = value.decode('utf-8')
        return jsonify({'key': key, 'value': value.decode('utf-8')})
    else:
        return jsonify({'message': 'Key not found'}), 404
if __name__ == '__main__':
    app.run()
