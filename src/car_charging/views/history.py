import os
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from car_charging.forms import DateRangeForm
from car_charging.models import ChargingSession, EnergyDetails, ZaptecToken
from .utils import request_charge_history, convert_datetime


def charge_history(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DateRangeForm(request.POST)
        if form.is_valid():
            access_token = ZaptecToken.objects.first().token
            installation_id = os.getenv("INSTALLATION_ID", "")
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            response = request_charge_history(access_token, installation_id, start_date, end_date)
            data = response.json()

            new_sessions = []
            for session_data in data["Data"]:
                session, is_created = ChargingSession.objects.get_or_create(
                    charger_id=session_data["ChargerId"],
                    commit_end_date_time=convert_datetime(session_data["CommitEndDateTime"] + "+00:00"),
                    commit_metadata=session_data["CommitMetadata"],
                    device_id=session_data["DeviceId"],
                    device_name=session_data["DeviceName"],
                    end_date_time=convert_datetime(session_data["EndDateTime"] + "+00:00"),
                    energy=session_data["Energy"],
                    externally_ended=session_data["ExternallyEnded"],
                    session_id=session_data["Id"],
                    start_date_time=convert_datetime(session_data["StartDateTime"] + "+00:00"),
                    user_email=getattr(session_data, "UserEmail", None),
                    user_full_name=getattr(session_data, "UserFullName", ""),
                    user_id=getattr(session_data, "UserId", None),
                    user_name=getattr(session_data, "UserName", None),
                )
                if not is_created:
                    continue

                new_sessions.append(session)
                for detail_data in session_data["EnergyDetails"]:
                    EnergyDetails.objects.create(
                        charging_session=session,
                        energy=detail_data["Energy"],
                        timestamp=convert_datetime(detail_data["Timestamp"]),
                    )
            return render(
                request,
                "car_charging/history.html",
                {
                    "new_sessions": new_sessions,
                    "new_sessions_count": len(new_sessions),
                    "form": form,
                    "data": data,
                },
            )
    else:
        form = DateRangeForm()
    return render(request, "car_charging/history.html", {"form": form})
