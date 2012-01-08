#!/bin/bash -x
# for development
SURVEYTOOL_HOME=$WORKON_HOME/surveytool/surveytool
python $SURVEYTOOL_HOME/manage.py runserver --settings=surveytool.conf.dev.settings

