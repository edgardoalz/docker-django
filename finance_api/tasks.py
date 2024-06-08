from celery import Celery
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

broker_url = env("BROKER_URL")

print(broker_url)

app = Celery('tasks', broker=broker_url, broker_connection_retry_on_startup=True)

@app.task
def add(x, y):
    return x + y