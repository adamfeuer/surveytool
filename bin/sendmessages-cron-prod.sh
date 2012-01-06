#!/bin/bash -x
SURVEYTOOL_ENV=/opt/webapps/research.liveingreatness.com
source $SURVEYTOOL_ENV/bin/activate
cd $SURVEYTOOL_ENV/surveytool
python $SURVEYTOOL_ENV/surveytool/manage.py cron send_messages --settings=surveytool.conf.prod.settings

