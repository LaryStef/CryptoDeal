from celery import Celery
from flask import Flask

from application import create_app

app: Flask
celery: Celery
app, celery = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
