import uuid
from django.test import TestCase
from django.utils.timezone import make_aware, timedelta, datetime
from car_charging.models import EnergyDetails, ChargingSession


class SpotPricesTest(TestCase):
    def setUp(self):
        self.price_area = 1
        self.time1 = make_aware(datetime(2022, 1, 1, 1, 0, 0))
        self.time2 = make_aware(datetime(2022, 1, 2, 1, 0, 0))
        self.time3 = make_aware(datetime(2022, 1, 3, 5, 0, 0))
        self.time4 = self.time3 + timedelta(hours=1)
        self.charger_id = uuid.uuid4()
        self.device_id = uuid.uuid4()
        self.session_id = uuid.uuid4()
        self.user_id_1 = uuid.uuid4()
        self.user_id_2 = uuid.uuid4()
        self.sessions = [
            ChargingSession.objects.create(
                user_id=self.user_id_1,
                user_name="User1",
                user_full_name="User Uno",
                user_email="user1@name.com",
                session_id=self.session_id,
                charger_id=self.charger_id,
                device_id=self.device_id,
                start_date_time=self.time1,
                end_date_time=self.time2,
                price_area=self.price_area,
                energy=1,
            ),
            ChargingSession.objects.create(
                user_id=self.user_id_2,
                user_name="User2",
                user_full_name="User Dos",
                user_email="user2@name.com",
                session_id=self.session_id,
                charger_id=self.charger_id,
                device_id=self.device_id,
                start_date_time=self.time2,
                end_date_time=self.time2 + timedelta(days=1),
                price_area=self.price_area,
                energy=2,
            ),
            ChargingSession.objects.create(
                # No user_id
                session_id=uuid.uuid4(),
                charger_id=self.charger_id,
                device_id=self.device_id,
                start_date_time=self.time3,
                end_date_time=self.time4,
                price_area=self.price_area,
                energy=3,
            ),
        ]
        self.energy_details = [
            EnergyDetails.objects.create(charging_session=self.sessions[0], timestamp=self.time1, energy=1.1),
            EnergyDetails.objects.create(charging_session=self.sessions[0], timestamp=self.time2, energy=2.2),
            EnergyDetails.objects.create(charging_session=self.sessions[1], timestamp=self.time2, energy=3.3),  # Has user_id_2
            EnergyDetails.objects.create(charging_session=self.sessions[2], timestamp=self.time3, energy=4.4),  # Has no user_id
            EnergyDetails.objects.create(charging_session=self.sessions[2], timestamp=self.time4, energy=5.5),  # Has no user_id
        ]

    def test_get_unique_users_returns_unique_users(self):
        """Test that get_unique_users returns all unique users."""
        users = ChargingSession.objects.get_unique_users()
        user1 = {
            "user_id": self.user_id_1,
            "user_full_name": "User Uno",
            "user_name": "User1",
            "user_email": "user1@name.com",
        }
        user2 = {
            "user_id": self.user_id_2,
            "user_full_name": "User Dos",
            "user_name": "User2",
            "user_email": "user2@name.com",
        }
        user3 = {"user_id": None, "user_full_name": "", "user_name": "", "user_email": None}

        self.assertIn(user1, users)
        self.assertIn(user2, users)
        self.assertIn(user3, users)
        self.assertEqual(len(users), 3)
