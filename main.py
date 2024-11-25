from celery import Celery
from flask import Flask

from app import create_app


app: Flask
celery: Celery
app, celery = create_app()
