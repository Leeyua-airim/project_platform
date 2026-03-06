from django.urls import path
from .views import health, enqueue_ping

urlpatterns = [
    path("health", health),
    path("tasks/ping", enqueue_ping),
]