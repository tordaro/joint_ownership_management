import uuid
from decimal import Decimal
from django.test import TestCase
from django.utils.timezone import make_aware, timedelta, datetime
from car_charging.models import SpotPrices, EnergyDetails, ChargingSession

from ..calculate import get_spot_prices, calculate_cost


class CalculateTest(TestCase):
    def setUp(self):
        self.price_area = 1
        self.price_area_name = f"no{self.price_area}"
        self.from_date = make_aware(datetime(2022, 1, 1, 1, 0, 0))
        self.to_date = make_aware(datetime(2022, 1, 2, 1, 0, 0))
        self.charger_id = uuid.uuid4()
        self.device_id = uuid.uuid4()
        self.session_id = uuid.uuid4()
        self.user_id_1 = uuid.uuid4()
        self.user_id_2 = uuid.uuid4()
        self.spot_prices = [
            SpotPrices.objects.create(start_time=self.from_date, end_time=self.to_date, **{self.price_area_name: 0.1}),
            SpotPrices.objects.create(start_time=self.to_date, end_time=self.to_date + timedelta(days=1), **{self.price_area_name: 0.2}),
        ]
        self.sessions = [
            ChargingSession.objects.create(
                user_id=self.user_id_1,
                session_id=self.session_id,
                charger_id=self.charger_id,
                device_id=self.device_id,
                start_date_time=self.from_date,
                end_date_time=self.to_date,
                price_area=self.price_area,
                energy=1,
            ),
            ChargingSession.objects.create(
                user_id=self.user_id_2,
                session_id=self.session_id,
                charger_id=self.charger_id,
                device_id=self.device_id,
                start_date_time=self.to_date,
                end_date_time=self.to_date + timedelta(days=1),
                price_area=self.price_area,
                energy=2,
            ),
        ]
        self.energy_details = [
            EnergyDetails.objects.create(charging_session=self.sessions[0], timestamp=self.from_date, energy=1.1),
            EnergyDetails.objects.create(charging_session=self.sessions[0], timestamp=self.to_date, energy=2.2),
            EnergyDetails.objects.create(charging_session=self.sessions[1], timestamp=self.to_date, energy=3.3),  # Has user_id_2
        ]

    def test_get_spot_prices(self):
        spot_price_map = get_spot_prices(self.from_date, self.to_date, self.price_area)

        self.assertEqual(spot_price_map[self.from_date], Decimal("0.1"))
        self.assertEqual(spot_price_map[self.to_date], Decimal("0.2"))

    def test_calculate_cost(self):
        spot_price_map = get_spot_prices(self.from_date, self.to_date, self.price_area)

        total_cost_user_1 = calculate_cost(spot_price_map, self.user_id_1, self.from_date, self.to_date)
        total_cost_user_2 = calculate_cost(spot_price_map, self.user_id_2, self.from_date, self.to_date)

        self.assertEqual(total_cost_user_1, Decimal("0.1") * Decimal("1.1") + Decimal("0.2") * Decimal("2.2"))
        self.assertEqual(total_cost_user_2, Decimal("3.3") * Decimal("0.2"))

    def calculate_session_cost(self):
        result = self.sessions[0].calculate_cost()
        expected_result = sum([energy_detail.calculate_cost() for energy_detail in self.energy_details[:2]])
        self.assertEqual(result, expected_result)

        result = self.sessions[1].calculate_cost()
        expected_result = sum([energy_detail.calculate_cost() for energy_detail in self.energy_details[2:]])
        self.assertEqual(result, expected_result)
