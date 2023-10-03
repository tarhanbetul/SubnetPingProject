# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task
from django.conf import settings
# Django ayarlarını projenize uygun şekilde ayarlayalım
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'subnet_project.settings')

# Celery uygulamasını oluşturun
celery_app = Celery('subnet_project')

# Celery yapılandırması
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Otomatik olarak görevleri bul ve kaydet
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#celery_app.autodiscover_tasks()
