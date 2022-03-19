import time
import tempfile

from google.cloud import bigquery
from google.cloud import storage

global times, bucket_students, bucket_teachers, big_query_client, client

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

    global bucket_students, bucket_teachers, big_query_client, client

    # Initialize Cloud Storage Bucket client
    client = storage.Client.from_service_account_json('../pliroforiaka-systimata-plir-account.json')
    # client = storage.Client()
    bucket_students = client.get_bucket('pliroforiaka-2022-students')
    bucket_teachers = client.get_bucket('pliroforiaka-2022-teachers')

    # Initialize Big Query client
    big_query_client = bigquery.Client.from_service_account_json('../pliroforiaka-systimata-plir-account.json')
    # big_query_client = bigquery.Client()

