# from flask import current_app
from .base import make_celery

async_client = make_celery()
