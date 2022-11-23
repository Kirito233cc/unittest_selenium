from test_celery import my_background_task

result = my_background_task.delay(1, 2)
print(result.id)

