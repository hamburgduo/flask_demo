#!/bin/bash

source /root/venv_employee/bin/activate

ps -ef | grep "python manage.py" | grep -v grep | awk '{print $2}' | xargs kill -9

python /var/lib/jenkins/workspace/employee/manage.py
