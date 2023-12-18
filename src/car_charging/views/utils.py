import requests
from django.utils.timezone import datetime


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


def convert_datetime(datetime_string):
    if "." in datetime_string:
        dt = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%f%z")
    else:
        dt = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S%z")
    return dt
