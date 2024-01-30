from django.utils.timezone import datetime
from django.db.models.functions import TruncHour

from car_charging.models import SpotPrices, EnergyDetails, ChargingSession


def get_spot_prices(from_date: datetime, to_date: datetime, price_area: int) -> dict:
    """
    Get spot prices for the given price area and date range, assuming that they exist.
    """
    price_area_name = f"no{price_area}"
    spot_prices = SpotPrices.objects.filter(start_time__gte=from_date, start_time__lte=to_date)

    spot_price_map = {}
    for price in spot_prices:
        spot_price_map[price.start_time] = getattr(price, price_area_name)

    return spot_price_map


def calculate_cost(spot_price_map: dict, user_id: str, from_date: datetime, to_date: datetime) -> float:
    """
    Calculate the total cost of charging for the given user, date range and spot price map.
    The spot price map is a dictionary with hourly spot prices for the given date range, in a given price area.
    """
    user_sessions = ChargingSession.objects.filter(user_id=user_id, start_date_time__gte=from_date, start_date_time__lte=to_date)
    energy_details = EnergyDetails.objects.filter(charging_session__in=user_sessions).annotate(hour=TruncHour("timestamp"))

    total_cost = 0
    for detail in energy_details:
        hour = detail.hour
        energy_used = detail.energy
        spot_price = spot_price_map.get(hour)
        total_cost += energy_used * spot_price

    return total_cost
