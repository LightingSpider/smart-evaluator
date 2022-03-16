from flask import Flask
from flask_restx import Api
import time
import tempfile

from google.cloud import bigquery
from google.cloud import storage

global db, app, api, times, bucket_students, bucket_teachers, big_query_client

def measure_time(func):
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        times[func.__name__] = end - start
        # print(func.__name__, end - start)
        return result

    return wrap

def init():

    global bucket_students, bucket_teachers, big_query_client

    # Initialize Cloud Storage Bucket client
    # client = storage.Client.from_service_account_json('/home/airth/Documents/9οeksamino/pliroforiaka/smart-evaluator/pliroforiaka-systimata-2022-d75366a215b2.json')
    client = storage.Client()
    bucket_students = client.get_bucket('pliroforiaka-2022-students')
    bucket_teachers = client.get_bucket('pliroforiaka-2022-teachers')

    # Initialize Big Query client
    # big_query_client = bigquery.Client.from_service_account_json('/home/airth/Documents/9οeksamino/pliroforiaka/smart-evaluator/pliroforiaka-systimata-query-key.json')
    big_query_client = bigquery.Client()

    # Initialize Flask App
    global app, api
    app = Flask(__name__)
    api = Api(app=app, version="1.0", title="Smart Evaluator REST APIs")

    ALLOWED_EXTENSIONS = {'csv'}
    app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
    app.config['MAX_CONTENT_PATH'] = 7340032
    app.config['PROPAGATE_EXCEPTIONS'] = True

    return app
