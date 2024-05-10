import logging
from django.forms import Form
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.views.generic.edit import FormView

import car_charging.zaptec_services as zts
from car_charging.forms import DateRangeForm

logger = logging.getLogger("django")


class ChargeHistoryView(FormView):
    template_name = "car_charging/history.html"
    form_class = DateRangeForm
    success_url = reverse_lazy("charging:session_list")

    def form_valid(self, form: Form):
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]
        data = zts.get_charge_history_data(start_date, end_date)
        new_sessions = zts.create_charging_sessions(data)

        if not data:
            messages.info(self.request, "No data retrieved for the given date range.")
            return render(self.request, self.template_name, {"form": form})
        elif not new_sessions:
            messages.info(self.request, "Data retrieved but no new sessions created.")
            self.request.session["no_new_sessions"] = True
            return render(self.request, self.template_name, {"form": form})
        else:
            messages.success(self.request, f"{len(new_sessions)} new charging sessions created.")
            return super().form_valid(form)

    def form_invalid(self, form: Form):
        return super().form_invalid(form)
