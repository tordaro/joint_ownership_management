import uuid
from django.utils.timezone import make_aware, datetime
from django.test import TestCase
from car_charging.models import ChargingSession, SpotPrices, EnergyDetails


class EnergyDetailsTest(TestCase):
    def setUp(self):
        self.price_area = 1
        self.price_area_name = f"no{self.price_area}"
        self.datetime_1 = make_aware(datetime(2022, 1, 1, 1, 30, 45))
        self.datetime_2 = make_aware(datetime(2022, 1, 2, 1, 29, 15))
        self.charger_id = uuid.uuid4()
        self.device_id = uuid.uuid4()
        self.session_id = uuid.uuid4()
        self.user_id_1 = uuid.uuid4()
        self.user_id_2 = uuid.uuid4()
        self.spot_price = SpotPrices.objects.create(start_time=self.datetime_1, end_time=self.datetime_2, **{self.price_area_name: 0.1})
        self.session = ChargingSession.objects.create(
            user_id=self.user_id_1,
            session_id=self.session_id,
            charger_id=self.charger_id,
            device_id=self.device_id,
            start_date_time=self.datetime_1,
            end_date_time=self.datetime_2,
            price_area=self.price_area,
            energy=1,
        )
        self.energy_detail_1 = EnergyDetails.objects.create(
            charging_session=self.session, spot_price=self.spot_price, energy=5, timestamp=self.datetime_1
        )
        self.energy_detail_2 = EnergyDetails.objects.create(charging_session=self.session, energy=3, timestamp=self.datetime_2)

    def test_get_price_value(self):
        """Test that get_price returns the correct value."""
        self.assertEqual(self.energy_detail_1.get_price(), 0.1)

    def test_get_price_none(self):
        """Test that get_price returns None when spot_price is None."""
        self.assertFalse(self.energy_detail_2.get_price())

    def test_calculate_cost_value(self):
        """Test that get_price returns the correct value."""
        self.assertEqual(self.energy_detail_1.calculate_cost(), 0.1 * 5)

    def test_calculate_cost_none(self):
        """Test that get_price returns None when spot_price is None."""
        self.assertFalse(self.energy_detail_2.calculate_cost())

    def test_get_hour(self):
        """Test that get_hour returns the correct value."""
        self.assertEqual(self.energy_detail_1.get_hour(), self.datetime_1.replace(minute=0, second=0, microsecond=0))
        self.assertEqual(self.energy_detail_2.get_hour(), self.datetime_2.replace(minute=0, second=0, microsecond=0))
