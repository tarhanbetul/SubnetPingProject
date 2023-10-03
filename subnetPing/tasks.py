# tasks.py
from celery import Celery
from .models import PingResult
from django.core.cache import cache
app = Celery('subnetPing')
from celery import shared_task

@shared_task
def process_subnet_ips(ip_address, is_active):
    try:
        ping_log = PingResult(ip_address=ip_address, is_active=is_active)
        ping_log.save()


    except Exception as e:
        raise e
@shared_task
def process_subnet_ips_caching(ip_address, status):
    try:
        key = f'ip_status_{ip_address}'
        cache.set(key, status, timeout=None)  # timeout=None, süresiz saklama anlamına gelir
    except Exception as e:
        raise e