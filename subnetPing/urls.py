from django.urls import path
from . import views  

urlpatterns = [
    path('get_subnet_ips/', views.get_subnet_ips, name='get_subnet_ips')
]