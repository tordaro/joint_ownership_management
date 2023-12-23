from django.views.generic.list import ListView
from car_charging.models import EnergyDetails


class EnergyDetailsListView(ListView):
    model = EnergyDetails
    paginate_by = 15
    template_name = "car_charging/energy_detail_list.html"
    context_object_name = "energy_details"
