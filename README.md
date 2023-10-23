# redis-proxy
1. high level arch overview: 
Flask web server + cache (TTL) that is connected to the Redis db 

2. what the code does 

3. Algo Complexity of cache ops 

4. Instructions for how to run the proxy & tests 
- proxy: python3 redis_proxy.py
- unit tests: python3 -m unittest redis_proxy_test.py
- end to end tests: first run the proxy (python3 redis_proxy.py)
    in a new window - python3 test_e2e.py    // python -m unittest test_e2e

5. How long I spent on each part of the project

6. A list of reqs I didn't implement / why (hopefully none isa)


misc notes: 
https://cachetools.readthedocs.io/en/latest/
- using TTL cache w max size parameter
-Redis - atomic operations 

