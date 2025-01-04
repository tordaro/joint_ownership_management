from decimal import Decimal
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.timezone import make_aware, datetime
from car_charging.models import SpotPriceRefund


class SpotPriceRefundTests(TestCase):
    def setUp(self) -> None:
        self.datetime_1 = make_aware(datetime(2024, 3, 1, 6))
        self.threshold = Decimal("0.75")
        self.reduction = Decimal("0.9")
        self.spot_price_refund_1 = SpotPriceRefund.objects.create(
            deduction_threshold=self.threshold, reduction_factor=self.reduction, start_date=self.datetime_1.date()
        )

    def test_calculate_refund(self):
        """Test that the get price method returns correct price."""
        price_above_threshold = self.threshold + Decimal("0.3")
        price_below_threshold = self.threshold - Decimal("0.2")
        refund_above_threshold = (price_above_threshold - self.threshold) * self.reduction
        refund_below_threshold = Decimal("0")

        returned_refund_above_threshold = self.spot_price_refund_1.calculate_refund_price(self.datetime_1, price_above_threshold)
        returned_refund_below_threshold = self.spot_price_refund_1.calculate_refund_price(self.datetime_1, price_below_threshold)

        self.assertEqual(returned_refund_above_threshold, refund_above_threshold)
        self.assertEqual(returned_refund_below_threshold, refund_below_threshold)

    def test_get_price_validation_error(self):
        """Test that the get price method raises a validation error if the timestamp is less than the start date."""
        datetime_2 = make_aware(datetime(2024, 2, 29, 10))

        with self.assertRaises(ValidationError):
            self.spot_price_refund_1.calculate_refund_price(datetime_2, Decimal("0.9"))
