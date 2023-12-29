from decimal import Decimal
from django.test import TestCase
from django.utils.timezone import datetime, make_aware
from unittest.mock import patch
from car_charging.models import SpotPrices
from car_charging.hks_services import request_spot_prices, get_or_request_daily_prices, SpotPriceRequestFailed


class TestSpotPrices(TestCase):
    def setUp(self):
        self.time_stamp = make_aware(datetime(2022, 1, 1, 1, 30))
        self.price_area = 4
        self.price_area_name = f"no{self.price_area}"
        self.spot_price = SpotPrices.objects.create(
            start_time=make_aware(datetime(2022, 1, 1, 1, 0)), end_time=make_aware(datetime(2022, 1, 1, 2, 0)), no4=0.255392
        )

    @patch("requests.get")
    def test_request_spot_prices(self, mock_get):
        mock_get.return_value.status_code = 200
        response = request_spot_prices(self.time_stamp, self.price_area)
        self.assertEqual(response.status_code, 200)

    def test_get_or_request_daily_prices_exists(self):
        price = get_or_request_daily_prices(self.spot_price.start_time, self.price_area)
        self.assertAlmostEqual(price, Decimal(getattr(self.spot_price, self.price_area_name)), places=6)

    @patch("requests.get")
    def test_get_or_request_daily_prices_request(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "NOK_per_kWh": 0.25539,
                "EUR_per_kWh": 0.02266,
                "EXR": 11.2705,
                "time_start": "2023-12-27T00:00:00+01:00",
                "time_end": "2023-12-27T01:00:00+01:00",
            },
            {
                "NOK_per_kWh": 0.25573,
                "EUR_per_kWh": 0.02269,
                "EXR": 11.2705,
                "time_start": "2023-12-27T01:00:00+01:00",
                "time_end": "2023-12-27T02:00:00+01:00",
            },
            {
                "NOK_per_kWh": 0.25516,
                "EUR_per_kWh": 0.02264,
                "EXR": 11.2705,
                "time_start": "2023-12-27T02:00:00+01:00",
                "time_end": "2023-12-27T03:00:00+01:00",
            },
        ]
        time_stamp = make_aware(datetime(year=2023, month=12, day=27, hour=1, minute=30))
        price = get_or_request_daily_prices(time_stamp, self.price_area)
        self.assertAlmostEqual(price, Decimal(0.25573), places=6)

    @patch("requests.get")
    def test_get_or_request_daily_prices_fail(self, mock_get):
        mock_get.return_value.status_code = 404
        time_stamp = make_aware(datetime(year=2023, month=12, day=27, hour=1, minute=30))
        with self.assertRaises(SpotPriceRequestFailed):
            get_or_request_daily_prices(time_stamp, self.price_area)
