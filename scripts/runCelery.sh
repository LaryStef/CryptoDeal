#!/bin/bash

echo celery starting...
.venv/bin/python -m celery -A main.celery beat &
.venv/bin/python -m celery -A main.celery worker -l INFO &
