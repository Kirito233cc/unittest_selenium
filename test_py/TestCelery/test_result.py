from celery.result import AsyncResult
from test_celery import celery

async_result = AsyncResult(id='1c38d404-e1e2-418d-aa07-187d5d96f094', app=celery)

if async_result.successful():
    result = async_result.get()
    print(result)
