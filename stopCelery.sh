#!/bin/bash

pkill -f "beat"
pkill -f "celery"
echo celery stopped
