from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import make_aware, datetime
from car_charging.models import SpotPrice


class SpotPricesTests(TestCase):
    """Test the spot price methods."""

    def setUp(self) -> None:
        self.nok_pr_kwh = Decimal("0.22")
        self.exchange_rate = Decimal("11.34")
        self.price_area = 2
        self.hour_stamp = make_aware(datetime(2024, 2, 8, 12))
        self.spot_price = SpotPrice.objects.create(
            nok_pr_kwh=self.nok_pr_kwh,
            eur_pr_kwh=self.nok_pr_kwh / self.exchange_rate,
            exchange_rate=self.exchange_rate,
            price_area=self.price_area,
            start_time=self.hour_stamp,
            end_time=self.hour_stamp.replace(hour=13),
        )

    def test_get_price_returns_correct_price(self):
        """Test that the get price method returns the correct price."""
        nok_pr_kwh = self.spot_price.get_price(timestamp=self.hour_stamp, price_area=self.price_area)

        self.assertEqual(nok_pr_kwh, self.nok_pr_kwh)

    def test_get_price_raises_time_validation_error(self):
        """Test that the get price method raises a validation error when given timestamp smaller than own start time."""
        too_soon = make_aware(datetime(2024, 2, 8, 11))

        with self.assertRaises(ValidationError):
            self.spot_price.get_price(timestamp=too_soon, price_area=self.price_area)

    def test_get_price_raises_price_area_validation_error(self):
        """Test that the get price method raises a validation error when given wrong price area."""
        other_price_area = 5

        with self.assertRaises(ValidationError):
            self.spot_price.get_price(timestamp=self.hour_stamp, price_area=other_price_area)
