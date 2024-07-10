from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from car_charging.models import EnergyDetails
from django.contrib.auth.mixins import LoginRequiredMixin

from car_charging.models import ChargingSession


class EnergyDetailsListView(LoginRequiredMixin, ListView):
    model = EnergyDetails
    template_name = "car_charging/energy_details.html"
    context_object_name = "energy_details"

    def get_queryset(self):
        qs = EnergyDetails.objects.select_related("charging_session")

        session_id = self.request.GET.get("session_id")
        if session_id:
            qs = qs.filter(charging_session=session_id)

        if self.request.user.is_staff:
            return qs
        else:
            return qs.filter(charging_session__user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get("session_id")
        if session_id:
            context["charging_session"] = get_object_or_404(ChargingSession, id=session_id)
        return context
