from django.urls import path

from car_charging.views import history, index, auth_token


urlpatterns = [
    path("", index, name="index"),
    path("history", history.charge_history, name="history"),
    path("token", auth_token.token_status, name="token_status"),
    path("renew_token", auth_token.renew_token, name="renew_token"),
]
