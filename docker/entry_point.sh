#!/bin/bash
echo Starting bbsparse.

service cron start

cd /bbsparse
python manage.py runserver 0.0.0.0:8001 > /data/bbsparse/logs/console.log 2>&1
