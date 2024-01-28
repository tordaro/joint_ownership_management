import uuid
from django.test import TestCase
from django.db.models.functions import TruncHour
from django.utils.timezone import make_aware, timedelta, datetime
from car_charging.models import SpotPrices, EnergyDetails, ChargingSession

from ..calculate import get_spot_prices, calculate_cost


class CalculateTest(TestCase):
    def setUp(self):
        self.price_area = 1
        self.price_area_name = f"no{self.price_area}"
        self.from_date = make_aware(datetime(2022, 1, 1, 1, 0, 0))
        self.to_date = make_aware(datetime(2022, 1, 2, 1, 0, 0))
        self.user_id = "test_user"
        self.charger_id = uuid.uuid4()
        self.device_id = uuid.uuid4()
        self.session_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.spot_prices = [
            SpotPrices.objects.create(start_time=self.from_date, end_time=self.to_date, **{self.price_area_name: 10}),
            SpotPrices.objects.create(start_time=self.to_date, end_time=self.to_date + timedelta(days=1), **{self.price_area_name: 20}),
        ]
        self.sessions = [
            ChargingSession.objects.create(
                user_id=self.user_id,
                session_id=self.session_id,
                charger_id=self.charger_id,
                device_id=self.device_id,
                start_date_time=self.from_date,
                end_date_time=self.to_date,
                energy=1,
            ),
            ChargingSession.objects.create(
                user_id=self.user_id,
                session_id=self.session_id,
                charger_id=self.charger_id,
                device_id=self.device_id,
                start_date_time=self.to_date,
                end_date_time=self.to_date + timedelta(days=1),
                energy=2,
            ),
        ]
        self.energy_details = [
            EnergyDetails.objects.create(charging_session=self.sessions[0], timestamp=self.from_date, energy=1),
            EnergyDetails.objects.create(charging_session=self.sessions[1], timestamp=self.to_date, energy=2),
        ]

    def test_get_spot_prices(self):
        hour = self.from_date

        spot_price_map = get_spot_prices(self.from_date, self.to_date, self.price_area)

        self.assertEqual(spot_price_map[hour], 10)

    def test_calculate_cost(self):
        spot_price_map = get_spot_prices(self.from_date, self.to_date, self.price_area)
        total_cost = calculate_cost(spot_price_map, self.user_id, self.from_date, self.to_date)
        self.assertEqual(total_cost, 1 * 10)
