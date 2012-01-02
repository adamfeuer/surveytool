#!/bin/bash -x
SURVEYTOOL_HOME=$WORKON_HOME/surveytool/surveytool
python $SURVEYTOOL_HOME/manage.py runserver --settings=surveytool.conf.dev.settings

