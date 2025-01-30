import uuid
from django.utils.timezone import datetime, make_aware
from django.test import TestCase
from decimal import Decimal
from car_charging.models import EnergyDetails, GridPrice, SpotPrice, SpotPriceRefund, UsagePrice, CostDetails, ChargingSession


class CostDetailsManagerTestCase(TestCase):
    """Unit tests for the filters and aggregations in the cost details manager."""

    def setUp(self):
        self.datetime_1 = make_aware(datetime(2025, 1, 1, 10))
        self.datetime_2 = make_aware(datetime(2025, 3, 1, 15))
        self.datetime_3 = make_aware(datetime(2025, 4, 1, 10))
        self.datetime_4 = make_aware(datetime(2025, 9, 1, 18))

        self.session_alice = ChargingSession.objects.create(
            user_full_name="Alice",  # relevant field
            user_id=uuid.uuid4(),  # relevant field
            session_id=uuid.uuid4(),
            charger_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            start_date_time=self.datetime_1,
            end_date_time=self.datetime_2,
            price_area=4,
            energy=2.31,
        )
        self.session_bert = ChargingSession.objects.create(
            user_full_name="Bert",  # relevant field
            user_id=uuid.uuid4(),  # relevant field
            session_id=uuid.uuid4(),
            charger_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            start_date_time=self.datetime_3,
            end_date_time=self.datetime_4,
            price_area=4,
            energy=2.31,
        )
        self.grid_price = GridPrice.objects.create(
            day_fee=Decimal("0.50"),
            night_fee=Decimal("0.30"),
            day_hour_from=6,
            night_hour_from=22,
            start_date=self.datetime_1.date(),
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
        self.spot_price_1 = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("0.55"),
            start_time=self.datetime_1,
            price_area=4,
        )
        self.spot_price_2 = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("0.49"),
            start_time=self.datetime_2,
            price_area=4,
        )
        self.spot_price_3 = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("1.11"),
            start_time=self.datetime_3,
            price_area=4,
        )
        self.spot_price_4 = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("0.67"),
            start_time=self.datetime_4,
            price_area=4,
        )
        self.energy_details_1 = EnergyDetails.objects.create(
            charging_session=self.session_alice,
            energy=Decimal("15.2"),
            timestamp=self.datetime_1,
        )
        self.energy_details_2 = EnergyDetails.objects.create(
            charging_session=self.session_bert,
            energy=Decimal("21.8"),
            timestamp=self.datetime_2,
        )
        self.energy_details_3 = EnergyDetails.objects.create(
            charging_session=self.session_alice,
            energy=Decimal("32.7"),
            timestamp=self.datetime_3,
        )
        self.energy_details_4 = EnergyDetails.objects.create(
            charging_session=self.session_bert,
            energy=Decimal("12.4"),
            timestamp=self.datetime_4,
        )

        CostDetails.objects.create(
            energy_detail=self.energy_details_1,
            spot_price=self.spot_price_1,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )
        CostDetails.objects.create(
            energy_detail=self.energy_details_2,
            spot_price=self.spot_price_2,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )
        CostDetails.objects.create(
            energy_detail=self.energy_details_3,
            spot_price=self.spot_price_3,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )
        CostDetails.objects.create(
            energy_detail=self.energy_details_4,
            spot_price=self.spot_price_4,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )


