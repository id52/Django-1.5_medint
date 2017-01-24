# - coding: utf-8  -
import sys

from fabric.api import local

APPS_TO_WATCH = ['common', 'medint', 'staff', 'messaging']


def initial():
#    apps = settings.INSTALLED_APPS
    for a in APPS_TO_WATCH:
        local('./manage.py convert_to_south %s' % a)


def migrate():
    for a in APPS_TO_WATCH:
        try:
            local('python manage.py migrate %s' % a)
        except:
            print  sys.exc_info()[0]
