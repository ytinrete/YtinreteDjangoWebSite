uwsgi --ini uwsgi.ini &
python3 manage.py celery worker --loglevel=info &
python3 ProcessWatcher.py > watch.txt &
