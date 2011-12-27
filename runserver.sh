#!/bin/bash -x
source $HOME/.surveytoolrc
python manage.py runserver --settings=surveytool.conf.dev.settings

