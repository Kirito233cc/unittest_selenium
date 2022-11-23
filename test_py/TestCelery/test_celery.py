from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery('test_celery', broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task()
def my_background_task(arg1, arg2):
    return arg1 + arg2



