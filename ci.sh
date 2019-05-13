#!/bin/bash

source /root/venv_employee/bin/activate

ps -ef | grep "python manage.py" | grep -v grep | awk '{print $2}' | xargs kill -9

nohup python /var/lib/jenkins/workspace/employee/manage.py >/var/lib/flask_web.log 2>&1 &