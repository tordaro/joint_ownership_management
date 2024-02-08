from django.test import TestCase
from django.utils.timezone import make_aware, datetime
from car_charging.models import SpotPrices


class SpotPricesTests(TestCase):
    def test_get_price_returns_price(self):
        hour_stamp = make_aware(datetime(2024, 2, 8, 12))
        spot_price = SpotPrices.objects.create(
            no1=0.1, no2=0.2, no3=0.3, no4=0.4, no5=0.5, start_time=hour_stamp, end_time=hour_stamp.replace(hour=13)
        )

        self.assertEqual(spot_price.get_price(1), 0.1)
        self.assertEqual(spot_price.get_price(2), 0.2)
        self.assertEqual(spot_price.get_price(3), 0.3)
        self.assertEqual(spot_price.get_price(4), 0.4)
        self.assertEqual(spot_price.get_price(5), 0.5)

    def test_get_price_raises_no_value_error(self):
        hour_stamp = make_aware(datetime(2024, 2, 8, 12))
        spot_price = SpotPrices.objects.create(start_time=hour_stamp, end_time=hour_stamp.replace(hour=13))

        with self.assertRaises(ValueError):
            spot_price.get_price(1)
        with self.assertRaises(ValueError):
            spot_price.get_price(2)
        with self.assertRaises(ValueError):
            spot_price.get_price(3)
        with self.assertRaises(ValueError):
            spot_price.get_price(4)
        with self.assertRaises(ValueError):
            spot_price.get_price(5)

    def test_get_price_raises_price_area_value_error(self):
        hour_stamp = make_aware(datetime(2024, 2, 8, 12))
        spot_price = SpotPrices.objects.create(start_time=hour_stamp, end_time=hour_stamp.replace(hour=13))

        with self.assertRaises(ValueError):
            spot_price.get_price(6)
        with self.assertRaises(ValueError):
            spot_price.get_price(0)
        with self.assertRaises(ValueError):
            spot_price.get_price(-1)

    def test_set_price_sets_price(self):
        hour_stamp = make_aware(datetime(2024, 2, 8, 12))
        spot_price = SpotPrices.objects.create(no4=0.4, start_time=hour_stamp, end_time=hour_stamp.replace(hour=13))

        spot_price.set_price(1, 0.1)
        spot_price.set_price(4, 0.2)

        self.assertEqual(spot_price.no1, 0.1)
        self.assertEqual(spot_price.no4, 0.2)

    def test_set_price_raises_error(self):
        hour_stamp = make_aware(datetime(2024, 2, 8, 12))
        spot_price = SpotPrices.objects.create(start_time=hour_stamp, end_time=hour_stamp.replace(hour=13))

        with self.assertRaises(ValueError):
            spot_price.set_price(6, 0.6)
        with self.assertRaises(ValueError):
            spot_price.set_price(0, 0.5)
        with self.assertRaises(ValueError):
            spot_price.set_price(-1, 0.5)
