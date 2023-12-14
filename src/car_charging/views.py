import os
import urllib3
from datetime import datetime
from urllib3.response import BaseHTTPResponse
from django.shortcuts import render
from django.utils import timezone

from car_charging.forms import DateRangeForm
from car_charging.models import ChargingSession, EnergyDetails


def index(request):
    return render(request, "car_charging/index.html")


def request_charge_history(access_token: str, installation_id: str, from_date: datetime, to_date: datetime) -> BaseHTTPResponse:
    """
    Request charge history from Zaptec API in given time interval.
    """
    datetime_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    endpoint_url = "https://api.zaptec.com/api/chargehistory"
    params = {
        "InstallationId": installation_id,
        "GroupBy": "2",
        "DetailLevel": "1",
        "From": from_date.strftime(datetime_format),
        "To": to_date.strftime(datetime_format),
    }
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json-patch+json"}

    http = urllib3.PoolManager()
    response = http.request("GET", endpoint_url, headers=headers, fields=params)

    return response


def convert_datetime(datetime_string):
    dt = datetime.strptime(datetime_string + "+0000", "%Y-%m-%dT%H:%M:%S.%f%z")
    return dt


def charge_history(request):
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            access_token = os.getenv("ZAPTEC_TOKEN")
            installation_id = os.getenv("INSTALLATION_ID")
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            response = request_charge_history(access_token, installation_id, start_date, end_date)
            data = response.json()

            new_sessions = 0
            for session_data in data["Data"]:
                session, exists = ChargingSession.objects.get_or_create(
                    charger_id=session_data["ChargerId"],
                    commit_end_date_time=convert_datetime(session_data["CommitEndDateTime"]),
                    commit_metadata=session_data["CommitMetadata"],
                    device_id=session_data["DeviceId"],
                    device_name=session_data["DeviceName"],
                    end_date_time=convert_datetime(session_data["EndDateTime"]),
                    energy=session_data["Energy"],
                    externally_ended=session_data["ExternallyEnded"],
                    session_id=session_data["Id"],
                    start_date_time=convert_datetime(session_data["StartDateTime"]),
                    user_email=session_data["UserEmail"],
                    user_full_name=session_data["UserFullName"],
                    user_id=session_data["UserId"],
                    user_name=session_data["UserUserName"],
                )
                if exists:
                    continue

                new_sessions += 1
                for detail_data in session_data["EnergyDetails"]:
                    EnergyDetails.objects.create(
                        charging_session=session,
                        energy=detail_data["Energy"],
                        timestamp=timezone.datetime.strptime(detail_data["Timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                    )
            return render(request, "car_charging/charge_history.html", {"new_sessions": new_sessions})
    else:
        form = DateRangeForm()
    return render(request, "car_charging/charge_history.html", {"form": form})
