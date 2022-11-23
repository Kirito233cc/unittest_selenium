from celery import Celery
from flask import Flask
from celery_thing import celeryconfig
app = Flask(__name__)
celery_app = Celery(app.import_name, broker=celeryconfig.broker_url, backend=celeryconfig.result_backend)
celery_app.config_from_object(celeryconfig)