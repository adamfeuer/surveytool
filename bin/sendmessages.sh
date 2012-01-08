#!/bin/bash -x
# for development
SURVEYTOOL_HOME=$WORKON_HOME/surveytool/surveytool
python $SURVEYTOOL_HOME/manage.py cron send_messages --settings=surveytool.conf.dev.settings

