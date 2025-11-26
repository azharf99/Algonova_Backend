from django.conf import settings

if settings.DEBUG:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
