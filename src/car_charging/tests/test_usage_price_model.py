from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import make_aware, datetime
from car_charging.models import UsagePrice


class UsagePriceTests(TestCase):
    def setUp(self) -> None:
        self.datetime_1 = make_aware(datetime(2024, 3, 1, 6))
        self.usage_price_1 = UsagePrice.objects.create(nok_pr_kwh=Decimal("0.42"), start_date=self.datetime_1.date())

    def test_get_price(self):
        """Test that the get price method returns correct price."""
        price_2025 = self.usage_price_1.get_price(self.datetime_1)

        self.assertEqual(self.usage_price_1.nok_pr_kwh, price_2025)

    def test_get_price_validation_error(self):
        """Test that the get price method raises a validation error if the timestamp is less than the start date."""
        datetime_2 = make_aware(datetime(2024, 2, 29, 10))

        with self.assertRaises(ValidationError):
            self.usage_price_1.get_price(datetime_2)
