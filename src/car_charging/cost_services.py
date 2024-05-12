import logging
from datetime import datetime
from car_charging.models import SpotPrice, GridPrice, CostDetails, EnergyDetails

logger = logging.getLogger("django")


def create_cost_details(from_date: datetime | None = None, to_date: datetime | None = None) -> None:
    energy_details = EnergyDetails.objects.all().select_related("charging_session")
    spot_prices = SpotPrice.objects.all()
    grid_prices = GridPrice.objects.all()

    if from_date:
        energy_details = energy_details.filter(timestamp__gte=from_date)
        spot_prices = spot_prices.filter(start_time__gte=from_date)
        grid_price = grid_prices.filter(start_date__gte=from_date.date())
    if to_date:
        energy_details = energy_details.filter(timestamp__lte=to_date)
        spot_prices = spot_prices.filter(start_time__lte=to_date)
        grid_price = grid_prices.filter(start_date__lte=to_date.date())

    for energy_detail in energy_details:
        price_area = energy_detail.charging_session.price_area
        hourly_timestamp = energy_detail.get_hourly_timestamp()
        grid_price = grid_prices.filter(start_date__lte=energy_detail.timestamp.date()).first()
        spot_price = spot_prices.filter(price_area=price_area, start_time=hourly_timestamp).first()
        cost_detail = CostDetails.objects.create(energy_detail=energy_detail, spot_price=spot_price, grid_price=grid_price)
        logger.info(f"Inserted cost detail {cost_detail}.")
