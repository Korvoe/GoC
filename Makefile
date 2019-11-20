.ONESHELL:

install:
	@. bin/activate;
	@pip3 install -r requirements.txt;
	@wget http://download.redis.io/releases/redis-5.0.5.tar.gz;
	@tar xzf redis-5.0.5.tar.gz;
	@cd redis-5.0.5;
	@make;
	
