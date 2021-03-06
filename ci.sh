#!/bin/bash

source /root/venv_employee/bin/activate

ps -ef | grep manage.py | grep -v grep | awk '{print $2}' | xargs kill -9

export BUILD_ID=dontKillMe
nohup python /var/lib/jenkins/workspace/employee/manage.py > /var/log/flask_web.log 2>&1 &
sleep 10s
