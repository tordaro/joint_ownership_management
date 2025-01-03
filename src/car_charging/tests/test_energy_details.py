import uuid
from django.utils.timezone import make_aware, datetime, timedelta
from django.test import TestCase
from car_charging.models import ChargingSession, EnergyDetails


class EnergyDetailsTests(TestCase):
    def setUp(self):
        self.price_area = 1
        self.price_area_name = f"no{self.price_area}"
        self.datetime_1 = make_aware(datetime(2022, 1, 1, 1, 30, 45))
        self.datetime_2 = make_aware(datetime(2022, 1, 2, 5, 29, 15))
        self.datetime_3 = self.datetime_2 + timedelta(hours=10)
        self.user_id_1 = uuid.uuid4()
        self.user_id_2 = uuid.uuid4()
        self.session_1 = ChargingSession.objects.create(
            user_id=self.user_id_1,
            user_full_name="Mr. Bojangles",
            session_id=uuid.uuid4(),
            charger_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            start_date_time=self.datetime_1,
            end_date_time=self.datetime_1 + timedelta(hours=2),
            price_area=self.price_area,  # TODO: delete
            energy=5,
        )
        self.session_2 = ChargingSession.objects.create(
            user_id=self.user_id_2,
            user_full_name="Per Vers",
            session_id=uuid.uuid4(),
            charger_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            start_date_time=self.datetime_2,
            end_date_time=self.datetime_2 + timedelta(hours=2),
            price_area=self.price_area,  # TODO: delete
            energy=2.3,
        )
        self.energy_detail_1 = EnergyDetails.objects.create(charging_session=self.session_1, energy=5, timestamp=self.datetime_1)
        self.energy_detail_2 = EnergyDetails.objects.create(charging_session=self.session_2, energy=1.1, timestamp=self.datetime_2)
        self.energy_detail_3 = EnergyDetails.objects.create(charging_session=self.session_2, energy=1.2, timestamp=self.datetime_3)
        self.energy_details = [self.energy_detail_1, self.energy_detail_2, self.energy_detail_3]

    def test_get_hourly_timestamp(self):
        """Test that get_hourly_timestamp returns timestamp with hourly precision."""
        datetime_1_hourly = self.datetime_1.replace(minute=0, second=0, microsecond=0)
        datetime_2_hourly = self.datetime_2.replace(minute=0, second=0, microsecond=0)
        datetime_3_hourly = self.datetime_3.replace(minute=0, second=0, microsecond=0)

        self.assertEqual(self.energy_detail_1.get_hourly_timestamp(), datetime_1_hourly)
        self.assertEqual(self.energy_detail_2.get_hourly_timestamp(), datetime_2_hourly)
        self.assertEqual(self.energy_detail_3.get_hourly_timestamp(), datetime_3_hourly)
