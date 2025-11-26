from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings

if settings.DEBUG:
    from celery import Celery

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Algonova_Backend.settings')

    app = Celery('Algonova_Backend')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
