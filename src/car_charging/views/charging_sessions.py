from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from car_charging.models import ChargingSession


@login_required
def charging_sessions(request):
    user = request.user

    if user.is_staff:
        sessions = ChargingSession.objects.all()
    else:
        sessions = ChargingSession.objects.filter(user_id=user.id)

    context = {
        "charging_sessions": sessions,
    }
    return render(request, "car_charging/charging_sessions.html", context)
