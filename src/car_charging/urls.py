from django.urls import path

from car_charging.views import history, index

urlpatterns = [
    path("", index, name="index"),
    path("history", history.charge_history, name="history"),
]
