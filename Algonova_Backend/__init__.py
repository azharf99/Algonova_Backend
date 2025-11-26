import os
from dotenv import load_dotenv
load_dotenv()


if os.getenv("DEBUG").lower() == "true":
    from .celery import app as celery_app
    __all__ = ('celery_app',)
