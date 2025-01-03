import uuid
from django.utils.timezone import datetime, make_aware
from django.test import TestCase
from car_charging.models import EnergyDetails, GridPrice, SpotPrice, SpotPriceRefund, UsagePrice, CostDetails
from decimal import Decimal

from car_charging.models.ChargingSession import ChargingSession


class CostDetailsTestCase(TestCase):

    def setUp(self):
        self.datetime_1 = make_aware(datetime(2025, 1, 1, 10))
        self.datetime_2 = make_aware(datetime(2025, 1, 1, 15))

        self.grid_price = GridPrice.objects.create(
            day_fee=Decimal("0.50"), night_fee=Decimal("0.30"), day_hour_from=6, night_hour_from=22, start_date=self.datetime_1.date()
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
        self.energy_details = EnergyDetails.objects.create(charging_session=self.charging_session, energy=Decimal("15.5"), timestamp=self.datetime_1)
        self.usage_price = UsagePrice.objects.create(nok_pr_kwh=Decimal("0.40"), start_date=self.datetime_1.date())
        self.spot_price_refund = SpotPriceRefund.objects.create(
            deduction_threshold=Decimal("0.35"), reduction_factor=Decimal("0.1"), start_date=self.datetime_1.date()
        )
        self.spot_price = SpotPrice.objects.create(nok_pr_kwh=Decimal("0.45"), start_time=self.datetime_1, price_area=4)

        self.cost_details = CostDetails.objects.create(
            energy_detail=self.energy_details,
            spot_price=self.spot_price,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )
        self.cost_details.save()

    def test_cost_details_initialization(self):
        """Test initialization of CostDetails model."""
        self.assertEqual(self.cost_details.energy_detail, self.energy_details)
        self.assertEqual(self.cost_details.grid_price, self.grid_price)
        self.assertEqual(self.cost_details.usage_price, self.usage_price)
        self.assertEqual(self.cost_details.spot_price_refund, self.spot_price_refund)

    # def test_cost_details_calculation(self):
    #     """Test that total cost is correctly calculated."""
    #     self.cost_details.save()  # Trigger the calculation methods
    #
    #     expected_total_cost = (
    #         self.energy_details.energy * self.grid_price.get_price(self.energy_details.timestamp)
    #         + self.energy_details.energy * self.usage_price.get_price(self.energy_details.timestamp)
    #         - self.energy_details.energy * self.spot_price_refund.calculate_refund_price(self.energy_details.timestamp, Decimal("0.40"))
    #     )
    #
    #     self.assertAlmostEqual(self.cost_details.total_cost, expected_total_cost, places=7)
    #
    def test_grid_price_update(self):
        """Test updating values in CostDetails model."""
        self.cost_details.grid_price = self.grid_price
        self.cost_details.save()

        self.assertEqual(self.cost_details.grid_price, self.grid_price)

    def test_set_grid_price(self):
        """Test the grid price set method."""
        grid_price = self.grid_price.get_price(self.datetime_1)

        self.assertEqual(self.cost_details.grid_price_nok, grid_price)

    def test_cost_details_string_representation(self):
        """Test the string representation of CostDetails model."""
        expected_str = str(self.cost_details.energy_detail.id)
        self.assertEqual(str(self.cost_details), expected_str)
