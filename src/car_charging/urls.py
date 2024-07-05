from django.urls import path

from car_charging.views import home, charging_sessions

app_name = "charging"

urlpatterns = [
    path("", home, name="home"),
    path("charging_sessions", charging_sessions, name="charging_sessions"),
    # path("token", auth_token.token_status, name="token_status"),
    # path("renew_token", auth_token.renew_token, name="renew_token"),
    # path("history", history.ChargeHistoryView.as_view(), name="history"),
    # path("sessions", ChargingSessionListView.as_view(), name="session_list"),
    # path("energy", EnergyDetailsListView.as_view(), name="energy_detail_list"),
]
