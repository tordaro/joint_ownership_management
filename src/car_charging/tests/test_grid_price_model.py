from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import make_aware, datetime
from car_charging.models import GridPrice


class GridPriceTests(TestCase):
    """Test the grid price model methods."""

    def setUp(self) -> None:
        self.datetime_1 = make_aware(datetime(2024, 3, 1, 6))
        self.grid_price_1 = GridPrice.objects.create(
            day_fee=Decimal("0.50"), night_fee=Decimal("0.30"), day_hour_from=6, night_hour_from=22, start_date=self.datetime_1.date()
        )

    def test_get_day_price(self):
        """Test that the get price method returns daytime fee."""
        price_2024 = self.grid_price_1.get_price(self.datetime_1)

        self.assertEqual(self.grid_price_1.day_fee, price_2024)

    def test_get_night_price(self):
        """Test that the get price method returns nighttime fee."""
        datetime_night = make_aware(datetime(2025, 1, 1, 22))
        price_2025 = self.grid_price_1.get_price(datetime_night)

        self.assertEqual(self.grid_price_1.night_fee, price_2025)

    def test_get_price_validation_error(self):
        """Test that the get price method raises a validation error if the timestamp is less than the start date."""
        datetime_too_early = make_aware(datetime(2024, 2, 29, 10))

        with self.assertRaises(ValidationError):
            self.grid_price_1.get_price(datetime_too_early)
