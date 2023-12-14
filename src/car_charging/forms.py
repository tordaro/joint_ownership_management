from django import forms
from django.utils.translation import gettext_lazy as _


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label=_("Start Date"), widget=forms.DateInput(attrs={"type": "date"}), localize=True)
    end_date = forms.DateField(label=_("End Date"), widget=forms.DateInput(attrs={"type": "date"}), localize=True)
