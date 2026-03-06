import os
from celery import Celery

# Django settings 모듈을 Celery에서 사용할 수 있도록 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery("platform_git")

# Django settings에서 CELERY로 시작하는 설정을 가져와서 Celery 설정으로 사용
app.config_from_object("django.conf:settings", namespace="CELERY")
# Celery가 Django 앱에서 task를 자동으로 발견하도록 설정
app.autodiscover_tasks()
