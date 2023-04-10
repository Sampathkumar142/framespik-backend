# framespik-backend
Photostudios and Event organizers management  service providing Organization.
CELERY_TASK_DEFAULT_QUEUE = 'myqueue'
celery -A framespik worker -l info -f celery.log --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo

to start the celery worker

to start the beat 
celery -A framespik beat