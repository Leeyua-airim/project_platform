# apps/api/users/urls.py
# users 앱의 API URL 정의

from django.urls import path
from .views import MeView

urlpatterns = [
    path("me", MeView.as_view(), name="me"),
]