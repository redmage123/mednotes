from django.urls import path
from . import views

urlpatterns = [
    path("config", views.config, name="config")
]

