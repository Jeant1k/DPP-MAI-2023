from celery import shared_task

# Пример асинхронной задачи Celery.
@shared_task
def add(x, y):
    return x + y
