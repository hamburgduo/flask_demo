#!/bin/bash

cd /var/lib/jenkins/workspace/employee
ps -ef | grep "python manage.py" | grep -v grep | awk '{print $2}' | xargs kill -9
python manage.py
