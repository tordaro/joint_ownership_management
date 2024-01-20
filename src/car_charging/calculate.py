from django.utils.timezone import datetime

from car_charging.models import SpotPrices


def get_spot_prices(from_date: datetime, to_date: datetime, price_area: int) -> dict:
    price_area_name = f"no{price_area}"
    spot_prices = SpotPrices.objects.filter(start_time__gte=from_date, end_time__lte=to_date)

    spot_price_map = {}
    for price in spot_prices:
        spot_price_map[price.hour] = getattr(price, price_area_name)

    return spot_price_map
