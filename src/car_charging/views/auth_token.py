import os
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.http import require_POST

from car_charging.models import ZaptecToken


def request_token(username: str, password: str) -> requests.Response:
    url = "https://api.zaptec.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "password", "username": username, "password": password}

    response = requests.post(url, data=data, headers=headers)
    return response


def token_status(request: HttpRequest) -> HttpResponse:
    token = ZaptecToken.objects.first()
    context = {
        "token_expired": token.is_token_expired() if token else True,
        "is_token_renewed": False,
        "msg": "No token found." if not token else "Token not expired.",
    }
    return render(request, "car_charging/token.html", context)


@require_POST
def renew_token(request: HttpRequest) -> HttpResponse:
    username = os.getenv("ZAPTEC_USERNAME", "")
    password = os.getenv("ZAPTEC_PASSWORD", "")
    response = request_token(username, password)

    context = {"token_expired": True, "is_token_renewed": False, "msg": ""}

    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get("access_token", "")
        token_type = response_data.get("token_type", "")
        expires_in = response_data.get("expires_in", None)
        zaptec_token, is_created = ZaptecToken.objects.get_or_create(
            token=token,
            token_type=token_type,
            expires_in=expires_in,
        )
        if is_created:
            context["is_token_renewed"] = True
            context["msg"] = "Token renewed"
        else:
            context["token_expired"] = zaptec_token.is_token_expired()
    else:
        context["msg"] = "Failed to renew token"

    return render(request, "car_charging/token.html", context)
