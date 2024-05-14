from django.test import TestCase
from django.utils.timezone import make_aware, datetime
from car_charging.models import SpotPrice


class SpotPricesTests(TestCase):
    def test_get_price_returns_price(self):
        price_area = 2
        hour_stamp = make_aware(datetime(2024, 2, 8, 12))
        spot_price = SpotPrice.objects.create(
            nok_pr_kwh=0.2,
            eur_pr_kwh=0.2 / 11.3,
            exchange_rate=11.3,
            price_area=price_area,
            start_time=hour_stamp,
            end_time=hour_stamp.replace(hour=13),
        )

        self.assertEqual(spot_price.get_price(timestamp=hour_stamp, price_area=price_area), 0.2)
