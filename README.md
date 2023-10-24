# redis-proxy
High Level Architectural & Code Overview

Python and Flask web Framework for Redis Proxy service:
This Python application uses the Flask web framework to create a Redis proxy service with caching. The service exposes a few endpoints to get and set (setting is primarily for testing purposes) data, & it uses a combination of an in memory cache (that was implemented using the cachetools module) & a Redis database for data storage. 

Approach: 
A client will send GET requests to the Flask web service, which will first check the TTL cache for the requested key. 
    - If the key is in the cache, the key/value pair are sent back to the client in the form of a JSON message. 
    - If the key isn't found in the cache, then the web service will query the Redis database. 
    - If the key is in the database, the key/value pair is sent back to the client, & if not a 'key not found' message is sent.
The web service will also update the TTL cache with the requested key & timestamp. If the cache becomes full, the LRU key is removed ; additionally, keys will automatically expire after a certain amount of time (both the time & cache capacity are configurable).

A connection to the Redis database is established using the redis.StrictRedis class. The redis host, port, & database are all configurable through the REDIS_HOST, REDIS_PORT, & REDIS_DB variables. 
A cache is initialized using the TTLCache from the cachetools library. The @cached decorator caches the results of the get_data function. This mechanism also contains a lock (cache_lock) to ensure thread safety in the case of sequential concurrent requests. Although Flask is single threaded by default, the use of this lock helps safeguard the caching operation from potential issues. 

The /set/<key>/<value> route is primarily used for testing, & allows clients to set data by providing a key & a value, which are stored in the cache. 
The /get/<key> route allows clients to request data associated with a certain key by using this route. This route calls the get_data function & returns the result as a JSON response. 

Complexity of Cache Operations: 

The cache is implemented using the cachetools.TTLCache from the cachetools library. The algorithmic complexity for several cache operations is described below: 

set_data : O(1) - For a TTLCache, setting an item is typically O(1), as it involves adding an item to a dictionary-like structure.

get_data (cached part): O(1) - The time complexity of retrieving an item from a TTLCache is O(1), because it involves looking up an item in a dictionary-like structure. 

cache eviction: O(1) - The cache eviction policy is triggered by both the TTL & LRU policies. Because the cache maintains data structures to quickly identify items that are candidates for eviction, the complexity for this process is O(1).

This complexity could potentially vary based on factors such as cache size, system resources, or server performance. Generally, most cache operations to access/insert/delete data are O(1). 


Instructions for how to run the proxy & tests: 
- proxy: python3 redis_proxy.py
- unit tests: python3 -m unittest redis_proxy_test.py
- end to end tests: first run the proxy (python3 redis_proxy.py)
    in a new window - python3 test_e2e.py    // python -m unittest test_e2e

Process Approach: 
First, I spent a couple of hours reading the specification & installing & importing the necessary libraries to begin implementing a solution. Then, I took another hour to familiarize myself with the concepts of routes, endpoints, & how Flask could work with the cache & database. After this, I spent an hour or so to look into the cachetools library - since it's a Python module, it made sense to use this library. Next, I used an LRU cache, and then reimplemented the cache using a TTL cache to satisfy the global expiry requirement, because the TTL cache is built upon the LRU cache. For the total project, I spent between 8-10 hours to complete it - including research, implementation, debugging, & testing.

A list of reqs I didn't implement / why : N/A

Here are some sources I found helpful when implementing this project:

https://cachetools.readthedocs.io/en/latest/
- using TTL cache w max size parameter
-Redis - atomic operations 

https://cachetools.readthedocs.io/en/stable/
- using @cached as a decorator 
(flask is a single threaded application - this is extra safety & to make sure that mulitple threads cant access the shared resource (the cache) at the same time)

https://flask-ptbr.readthedocs.io/en/latest/quickstart.html#:~:text=The%20if%20__name__,used%20as%20an%20imported%20module.
- quick intro to flask 



