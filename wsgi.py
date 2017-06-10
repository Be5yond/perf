#coding: utf-8
"""
WSGI config for comm comm.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import shutil
import celery.app
celery_app = celery.app.app_or_default()


reload(sys)
sys.setdefaultencoding('utf8')

from django.core.wsgi import get_wsgi_application
# setting_root = os.path.join(os.path.dirname(__file__),'root')
# print setting_root,'----------------------------'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings_test")
# shutil.copy(os.path.join(setting_root,'settings_test.py'), os.path.join(setting_root,'settings.py'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "perf.settings")
application = get_wsgi_application()
