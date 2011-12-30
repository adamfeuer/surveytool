#!/bin/bash -x
source $HOME/.surveytoolrc
SURVEYTOOL_ENV=$HOME/.virtualenvs/surveytool
source $SURVEYTOOL_ENV/bin/activate
cd $SURVEYTOOL_ENV/surveytool
python $SURVEYTOOL_ENV/surveytool/manage.py cron send_messages --settings=surveytool.conf.dev.settings

