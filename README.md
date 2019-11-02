1. Download the repository.
2. When you are in the repository activate the python virtual machine: 
    $ source bin/activate 
3. Install all the required python packages:
    $ pip install -r requirements.txt
        or
    $ pip3 install -r requirements.txt
4. Install Redis:
    $ wget http://download.redis.io/releases/redis-5.0.5.tar.gz
    $ tar xzf redis-5.0.5.tar.gz
5. Run Redis:
    $ cd redis-5.0.5
    $ make
    # src/redis-server
6. Run django server:
    $ cd web-chat
    $ python manage.py runserver
        or
    $ python3 manage.py runserver
    
