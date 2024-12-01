#!/bin/bash

echo celery starting...
.venv/bin/python -m celery -A main.celery beat -l INFO &
.venv/bin/python -m celery -A main.celery worker -l INFO &
