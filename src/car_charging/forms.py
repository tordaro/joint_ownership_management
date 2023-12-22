from django import forms
from django.utils.timezone import datetime, timedelta
from django.utils.translation import gettext_lazy as _


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label=_("Start Date"), widget=forms.DateInput(attrs={"type": "date"}), localize=True)
    end_date = forms.DateField(label=_("End Date"), widget=forms.DateInput(attrs={"type": "date"}), localize=True)

    def __init__(self, *args, **kwargs):
        super(DateRangeForm, self).__init__(*args, **kwargs)
        today = datetime.today().date()
        thirty_days_ago = today - timedelta(days=30)
        self.fields["start_date"].initial = thirty_days_ago
        self.fields["end_date"].initial = today
