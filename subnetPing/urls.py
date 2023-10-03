from django.urls import path
from . import views  # views dosyanızın adını ve yolu ile değiştirin

urlpatterns = [
    path('get_subnet_ips/', views.get_subnet_ips, name='get_subnet_ips'),
    path('hello-world/', views.hello_world, name='hello-world'),
]