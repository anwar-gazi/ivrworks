web: gunicorn core.wsgi

worker: celery worker -A core.celery_app -l debug
beat: celery beat -A core.celery_app -l debug