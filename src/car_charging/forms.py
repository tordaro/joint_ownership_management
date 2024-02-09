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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        today = datetime.today().date()

        # TODO: Test this
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError(_("Start date cannot be later than end date."))
            if start_date > today:
                raise forms.ValidationError(_("Start date cannot be later than today's date."))


class CSVUploadForm(forms.Form):
    file = forms.FileField()
