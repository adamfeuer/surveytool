#!/bin/bash -x
source $HOME/.surveytoolrc
python manage.py cron send_messages

