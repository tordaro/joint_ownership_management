from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("history", views.charge_history, name="history"),
]