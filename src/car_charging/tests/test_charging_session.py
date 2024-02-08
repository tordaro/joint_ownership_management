import uuid
from django.test import TestCase
from django.utils.timezone import make_aware, timedelta, datetime
from car_charging.models import SpotPrices, EnergyDetails, ChargingSession


class SpotPricesTest(TestCase):
    def setUp(self):
        self.price_area = 1
        self.price_area_name = f"no{self.price_area}"
        self.time1 = make_aware(datetime(2022, 1, 1, 1, 0, 0))
        self.time2 = make_aware(datetime(2022, 1, 2, 1, 0, 0))
        self.time3 = make_aware(datetime(2022, 1, 3, 5, 0, 0))
        self.time4 = self.time3 + timedelta(hours=1)
        self.charger_id = uuid.uuid4()
        self.device_id = uuid.uuid4()
        self.session_id = uuid.uuid4()
        self.user_id_1 = uuid.uuid4()
        self.user_id_2 = uuid.uuid4()
        self.spot_prices = [
            SpotPrices.objects.create(start_time=self.time1, end_time=self.time2, **{self.price_area_name: 0.1}),
            SpotPrices.objects.create(start_time=self.time2, end_time=self.time2 + timedelta(days=1), **{self.price_area_name: 0.2}),
            SpotPrices.objects.create(start_time=self.time3, end_time=self.time2, **{self.price_area_name: 0.3}),
            SpotPrices.objects.create(start_time=self.time4, end_time=self.time2, **{self.price_area_name: 0.4}),
        ]
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
        self.user1_cost = 0.1 * 1.1 + 0.2 * 2.2
        self.user2_cost = 0.2 * 3.3
        self.anynomous_user_cost = 0.3 * 4.4 + 0.4 * 5.5

        for energy_detail in self.energy_details:
            energy_detail.set_spot_price()

    def test_calculate_session_cost(self):
        """Test that the correct total cost of a charging session is calculated when all energy details have related prices."""
        session1_cost = self.sessions[0].calculate_cost()
        session2_cost = self.sessions[1].calculate_cost()

        self.assertEqual(session1_cost, 0.1 * 1.1 + 0.2 * 2.2)
        self.assertEqual(session2_cost, 3.3 * 0.2)

    def test_calculate_total_user_cost(self):
        """Test calculation of total cost for given users."""
        user1_cost = ChargingSession.objects.calculate_user_cost(user_id=self.user_id_1)
        user2_cost = ChargingSession.objects.calculate_user_cost(user_id=self.user_id_2)

        self.assertEqual(user1_cost, 0.1 * 1.1 + 0.2 * 2.2)
        self.assertEqual(user2_cost, 3.3 * 0.2)

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

    def test_calculate_total_cost_by_user(self):
        """Test that the total cost for a user is calculated correctly."""
        user1 = {
            "user_id": self.user_id_1,
            "user_full_name": "User Uno",
            "user_name": "User1",
            "user_email": "user1@name.com",
            "total_cost": self.user1_cost,
        }
        user2 = {
            "user_id": self.user_id_2,
            "user_full_name": "User Dos",
            "user_name": "User2",
            "user_email": "user2@name.com",
            "total_cost": self.user2_cost,
        }
        user3 = {"user_id": None, "user_full_name": "", "user_name": "", "user_email": None, "total_cost": self.anynomous_user_cost}

        user_costs = ChargingSession.objects.calculate_total_cost_by_user()

        self.assertIn(user1, user_costs)
        self.assertIn(user2, user_costs)
        self.assertIn(user3, user_costs)
        self.assertEqual(len(user_costs), 3)
