import requests
from django.utils.timezone import datetime, timedelta
from django.utils.dateparse import parse_datetime
from car_charging.models import SpotPrices


def request_spot_prices(timestamp: datetime, price_area: int) -> requests.Response:
    """
    Request daily prices from Hvakosterstrommen API for given date and price area.
    """
    url = "https://www.hvakosterstrommen.no/api/v1/prices/" + f"{timestamp.year}/{timestamp.month:0>2}-{timestamp.day:0>2}_NO{price_area}.json"
    response = requests.get(url)
    return response


class SpotPriceRequestFailed(Exception):
    """Exception raised when spot price request fails."""

    def __init__(self, date: datetime.date, price_area: int, status_code=None):
        self.date = date
        self.price_area = price_area
        self.message = f"Failed to get spot price for {date} in price area {price_area}."
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} - Status Code: {self.status_code}"


def get_or_request_daily_prices(time_stamp: datetime, price_area: int) -> float:
    """
    Get daily prices from the database if they exist, otherwise request them from Hvakosterstrommen API.
    """
    price_area_name = f"no{price_area}"
    time_stamp = time_stamp.replace(minute=0, second=0, microsecond=0)  # Prices are given hourly
    try:
        spot_price = SpotPrices.objects.get(start_time=time_stamp)
        return getattr(spot_price, price_area_name)
    except SpotPrices.DoesNotExist:
        response = request_spot_prices(time_stamp, price_area)
        if response.status_code == 200:
            price_data = response.json()
            for hourly_price in price_data:
                SpotPrices.objects.create(
                    start_time=parse_datetime(hourly_price.get("time_start")),
                    end_time=parse_datetime(hourly_price.get("time_end")),
                    **{price_area_name: hourly_price.get("NOK_per_kWh")},
                )
            spot_price = SpotPrices.objects.get(start_time=time_stamp)
            return getattr(spot_price, price_area_name)
        else:
            raise SpotPriceRequestFailed(time_stamp, price_area, response.status_code)


def set_spot_prices(date: datetime, price_area: int):
    response = request_spot_prices(date, price_area)
    if response.status_code == 200:
        price_data = response.json()
        for hourly_price in price_data:
            SpotPrices.objects.update_or_create(
                start_time=parse_datetime(hourly_price.get("time_start")),
                defaults={
                    "end_time": parse_datetime(hourly_price.get("time_end")),
                    **{f"no{price_area}": hourly_price.get("NOK_per_kWh")},
                },
            )
    else:
        raise SpotPriceRequestFailed(date.date(), price_area, response.status_code)


def populate_missing_spot_prices(start_date: datetime, end_date: datetime, price_area: int):
    populated_dates = []
    current_date = start_date

    while current_date <= end_date:
        if (
            not SpotPrices.objects.filter(start_time__date=current_date).exists()
            or SpotPrices.objects.filter(start_time__date=current_date, **{f"no{price_area}__isnull": True}).exists()
        ):
            try:
                set_spot_prices(current_date, price_area)
                populated_dates.append(current_date.date())
            except SpotPriceRequestFailed as e:
                print(e)  # Handle the exception as needed

        current_date += timedelta(days=1)

    return populated_dates
