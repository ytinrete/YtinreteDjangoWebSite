killall -9 uwsgi
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
ps auxww | grep 'ProcessWatcher' | awk '{print $2}' | xargs kill -9