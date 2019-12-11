Secure web-chat.

The aim of this project is to create a web-chat application, which focuses the users' privacy and security.

OS: Linux
Python version: 3.7.3

How to install:
1. $ cd directory/of/the/project/ 
2. $ make install (run make file to install requirements)
            or manually
1. $ cd directory/of/the/project/ 
2. $ source bin/activate or $ . bin/activate (run the python virtual environment)
3. $ pip install -r requirements.txt or $ pip3 install -r requirements.txt  (install python packages from requirements.txt)
4. $ wget http://download.redis.io/releases/redis-5.0.7.tar.gz (download and install redis)
5. $ tar xzf redis-5.0.7.tar.gz
5. $ cd redis-5.0.7
6. $ make or $ make MALLOC=libc (make redis)

How to run:
1. $ source bin/activate or $ . bin/activate 
2. $ src/redis-server (run redis server)
        open a new terminal tab or window
1. $ source bin/activate or $ . bin/activate
2. $ cd web-chat
3. $ python manage.py runserver or $ python3 manage.py runserver (run django server)
4. $ python manage.py crontab add or $ python3 manage.py crontab add (run cron jobs)
5. Open the 'localhost/8000' in your browser

FIXED:
1. [SoS] First attack: /redis-5.0.5
Changed the vulnerable redis-5.0.5 to more secure redis-5.0.7
2. [ASU] First Attack: X-XSS-Protection header 
Added X-XSS-Protection header
