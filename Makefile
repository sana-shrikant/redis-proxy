CACHE_SIZE = 2
CACHE_EXPIRY = 2

venv:
	python3 -m venv venv
run: venv
	. venv/bin/activate && python3 redis_proxy.py
test: venv populate_test_data
	. venv/bin/activate && python3 -m unittest discover redis_proxy -p '*_test.py'
setup: venv
	. venv/bin/activate && pip3 install -r requirements.txt
start-redis:
	redis-server
stop-redis:
	pkill redis-server
clean:
	rm -rf __pycache__
populate_test_data: venv
	. venv/bin/activate && python3 populate_test_data.py
