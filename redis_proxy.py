from flask import Flask, request, jsonify
import redis 
from cachetools import LRUCache
from cachetools import TTLCache, cached
from datetime import datetime
from threading import Lock

app = Flask(__name__)

#configuration settings: 
cache_max_size = 2 #testing purposes = 2 - configurable cache capacity
global_expiry_seconds = 2 #testing purposes = 2 - configurable cache expiry time

DEFAULT_HOST = '127.0.0.1' 
DEFAULT_PORT = 5000

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

cache_lock = Lock()
redis_client = redis.StrictRedis(host = REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
#cache = LRUCache(maxsize = 2) 
cache = TTLCache(maxsize = cache_max_size, ttl = global_expiry_seconds)


@app.route('/set/<key>/<value>', methods=['GET'])
#this is primarily for testing purposes
def set_data(key, value):
    cache[key] = value
    return ('', 204)
@cached(cache=cache, lock = cache_lock)
def get_data(key):
    #check the cache first
    cached_value = None
    
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
@app.route('/get/<key>', methods= ['GET'])
def get_data_route(key):
    response = get_data(key)
    return response

if __name__ == '__main__':
    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
