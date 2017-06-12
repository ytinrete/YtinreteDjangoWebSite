uwsgi --ini uwsgi.ini &
python3 manage.py celery worker --loglevel=info &
