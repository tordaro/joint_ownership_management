from django.views.generic.list import ListView
from car_charging.models import ChargingSession


class ChargingSessionListView(ListView):
    model = ChargingSession
    paginate_by = 10
    template_name = "car_charging/session_list.html"
    context_object_name = "sessions"
