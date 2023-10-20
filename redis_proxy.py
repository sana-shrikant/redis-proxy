from flask import Flask, request, jsonify
import redis 
from cachetools import LRUCache

app = Flask(__name__)

redis_client = redis.StrictRedis(host = 'localhost', port=6379, db=0)
cache = LRUCache(maxsize = 2) #TODO: figure out what this number should be - rn it's arbitrarily 1000 
@app.route('/set/<key>/<value>', methods=['GET'])
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
        if len(cache) >= cache.maxsize:
            #remove LRU item to make room for new one 
            cache.popitem()
        cache[key] = value.decode('utf-8')
        return jsonify({'key': key, 'value': value.decode('utf-8')})
    else:
        return jsonify({'message': 'Key not found'}), 404
if __name__ == '__main__':
    app.run()
