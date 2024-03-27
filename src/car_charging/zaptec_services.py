import requests
from datetime import datetime

from car_charging.models import ZaptecToken


def request_charge_history(access_token: str, installation_id: str, from_date: datetime, to_date: datetime) -> requests.Response:
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
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(endpoint_url, headers=headers, params=params)
    return response


def request_token(username: str, password: str) -> requests.Response:
    url = "https://api.zaptec.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "password", "username": username, "password": password}

    response = requests.post(url, data=data, headers=headers)
    return response


class TokenRenewalException(Exception):
    """Exception raised when token renewal fails."""

    def __init__(self, message: str = "Failed to renew Zaptec token", status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} - Status Code: {self.status_code}"


def renew_token(username: str, password: str) -> ZaptecToken:
    response = request_token(username, password)
    if response.status_code != 200:
        raise TokenRenewalException(status_code=response.status_code)

    response_data = response.json()
    new_token = ZaptecToken.objects.create(
        token=response_data.get("access_token", ""),
        token_type=response_data.get("token_type", ""),
        expires_in=response_data.get("expires_in", None),
    )
    return new_token
