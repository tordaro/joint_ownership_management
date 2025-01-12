import uuid
from django.utils.timezone import datetime, make_aware
from django.test import TestCase
from decimal import Decimal
from car_charging.models import EnergyDetails, GridPrice, SpotPrice, SpotPriceRefund, UsagePrice, CostDetails, ChargingSession


class CostServicesTestCase(TestCase):
    """Test case for the cost details services."""

    def setUp(self):
        self.datetime_1 = make_aware(datetime(2025, 1, 1, 10))
        self.datetime_2 = make_aware(datetime(2025, 1, 1, 15))

        self.grid_price = GridPrice.objects.create(
            day_fee=Decimal("0.50"),
            night_fee=Decimal("0.30"),
            day_hour_from=6,
            night_hour_from=22,
            start_date=self.datetime_1.date(),
        )
        self.charging_session = ChargingSession.objects.create(
            session_id=uuid.uuid4(),
            charger_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            start_date_time=self.datetime_1,
            end_date_time=self.datetime_2,
            price_area=4,
            energy=2.31,
        )
        self.energy_details = EnergyDetails.objects.create(
            charging_session=self.charging_session,
            energy=Decimal("15.5"),
            timestamp=self.datetime_1,
        )
        self.usage_price = UsagePrice.objects.create(
            nok_pr_kwh=Decimal("0.40"),
            start_date=self.datetime_1.date(),
        )
        self.spot_price_refund = SpotPriceRefund.objects.create(
            deduction_threshold=Decimal("0.35"),
            reduction_factor=Decimal("0.1"),
            start_date=self.datetime_1.date(),
        )
        self.spot_price = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("0.95"),
            start_time=self.datetime_1,
            price_area=4,
        )

        self.cost_details = CostDetails.objects.create(
            energy_detail=self.energy_details,
            spot_price=self.spot_price,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )
