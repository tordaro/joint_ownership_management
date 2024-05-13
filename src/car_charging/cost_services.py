import logging
from datetime import datetime
from car_charging.models import SpotPrice, GridPrice, CostDetails, EnergyDetails, UsagePrice

logger = logging.getLogger("django")


def create_cost_details(from_date: datetime | None = None, to_date: datetime | None = None) -> None:
    energy_details = EnergyDetails.objects.all().select_related("charging_session")
    spot_prices = SpotPrice.objects.all()
    grid_prices = GridPrice.objects.all()
    usage_prices = UsagePrice.objects.all()

    if from_date:
        energy_details = energy_details.filter(timestamp__gte=from_date)
        spot_prices = spot_prices.filter(start_time__gte=from_date)
        grid_price = grid_prices.filter(start_date__gte=from_date.date())
        usage_prices = usage_prices.filter(start_date__gte=from_date.date())
    if to_date:
        energy_details = energy_details.filter(timestamp__lt=to_date)
        spot_prices = spot_prices.filter(start_time__lt=to_date)
        grid_price = grid_prices.filter(start_date__lt=to_date.date())
        usage_prices = usage_prices.filter(start_date__lt=to_date.date())

    for energy_detail in energy_details:
        price_area = energy_detail.charging_session.price_area
        hourly_timestamp = energy_detail.get_hourly_timestamp()
        spot_price = spot_prices.filter(price_area=price_area, start_time=hourly_timestamp).first()  # Assuming ordering -start_time
        grid_price = grid_prices.filter(start_date__lte=energy_detail.timestamp.date()).first()  # Assuming ordering -start_date
        usage_price = usage_prices.filter(start_date__lte=energy_detail.timestamp.date()).first()  # Assuming ordering -start_date

        cost_detail, is_created = CostDetails.objects.get_or_create(
            energy_detail=energy_detail, spot_price=spot_price, grid_price=grid_price, usage_price=usage_price
        )
        if is_created:
            logger.info(f"Inserted cost detail {cost_detail}.")
