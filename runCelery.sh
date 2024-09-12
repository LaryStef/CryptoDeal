#!/bin/bash

echo celery starting...
.venv/bin/python -m celery -A run.celery beat &
.venv/bin/python -m celery -A run.celery worker -l INFO &
