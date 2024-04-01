import uuid
from django.utils.timezone import make_aware, datetime, timedelta
from django.test import TestCase
from car_charging.models import ChargingSession, SpotPrices, EnergyDetails


class EnergyDetailsTests(TestCase):
    def setUp(self):
        self.price_area = 1
        self.price_area_name = f"no{self.price_area}"
        self.datetime_1 = make_aware(datetime(2022, 1, 1, 1, 30, 45))
        self.datetime_2 = make_aware(datetime(2022, 1, 2, 1, 29, 15))
        self.datetime_3 = self.datetime_2 + timedelta(days=10)
        self.user_id_1 = uuid.uuid4()
        self.user_id_2 = uuid.uuid4()
        self.spot_price_1 = SpotPrices.objects.create(start_time=self.datetime_1, **{self.price_area_name: 0.1})
        self.spot_price_2 = SpotPrices.objects.create(start_time=self.datetime_2, **{self.price_area_name: 0.2})
        self.spot_price_3 = SpotPrices.objects.create(start_time=self.datetime_3, **{self.price_area_name: 0.3})
        self.session_1 = ChargingSession.objects.create(
            user_id=self.user_id_1,
            user_full_name="Mr. Bojangles",
            session_id=uuid.uuid4(),
            charger_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            start_date_time=self.datetime_1,
            end_date_time=self.datetime_1 + timedelta(hours=2),
            price_area=self.price_area,
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
            price_area=self.price_area,
            energy=2.3,
        )
        self.energy_detail_1 = EnergyDetails.objects.create(
            charging_session=self.session_1, spot_price=self.spot_price_1, energy=5, timestamp=self.datetime_1
        )
        self.energy_detail_2 = EnergyDetails.objects.create(
            charging_session=self.session_2, spot_price=self.spot_price_2, energy=1.1, timestamp=self.datetime_2
        )
        self.energy_detail_3 = EnergyDetails.objects.create(
            charging_session=self.session_2, spot_price=self.spot_price_3, energy=1.2, timestamp=self.datetime_3
        )
        self.energy_details = [self.energy_detail_1, self.energy_detail_2, self.energy_detail_3]

    def test_get_price_value(self):
        """Test that get_price returns the correct value."""
        self.assertEqual(self.energy_detail_1.get_price(), 0.1)

    def test_get_price_none(self):
        """Test that get_price raises ValueError when spot_price is None."""
        energy_detail = EnergyDetails.objects.create(charging_session=self.session_1, energy=3, timestamp=self.datetime_2)

        with self.assertRaises(ValueError):
            energy_detail.get_price()

    def test_calculate_cost_value(self):
        """Test that get_price returns the correct value."""
        self.assertEqual(self.energy_detail_1.calculate_cost(), 0.1 * 5)

    def test_calculate_cost_none(self):
        """Test that calculate_cost results in a ValueError the price is not available."""
        energy_detail = EnergyDetails.objects.create(charging_session=self.session_1, energy=3, timestamp=self.datetime_2)

        with self.assertRaises(ValueError):
            energy_detail.calculate_cost()

    def test_cost_auto_field(self):
        """Test that the non editable cost field is set with correct value."""
        self.assertFalse(self.energy_detail_1.cost)
        self.energy_detail_1.set_cost()
        self.assertEqual(self.energy_detail_1.cost, self.energy_detail_1.energy * self.spot_price_1.no1)

    def test_get_hour(self):
        """Test that get_hour returns the correct value."""
        self.assertEqual(self.energy_detail_1.get_hour(), self.datetime_1.replace(minute=0, second=0, microsecond=0))

    def test_set_spot_correct_price(self):
        """Test that set_spot_price sets correct spot price when available."""
        precise_timestamp = make_aware(datetime(2024, 2, 8, 10, 55, 49, 123))
        hour_timestamp = precise_timestamp.replace(minute=0, second=0, microsecond=0)
        energy_detail = EnergyDetails.objects.create(charging_session=self.session_1, timestamp=precise_timestamp, energy=4.4)
        spot_price = SpotPrices.objects.create(start_time=hour_timestamp, end_time=hour_timestamp.replace(hour=11), **{self.price_area_name: 0.4})

        energy_detail.set_spot_price()

        self.assertAlmostEqual(float(energy_detail.get_price()), spot_price.get_price(price_area=1), places=6)

    def test_set_spot_price_raises_error(self):
        """Test that set_spot_price raises error when no matching spot price exists."""
        precise_timestamp = make_aware(datetime(2024, 2, 8, 10, 55, 49, 123))
        hour_timestamp = precise_timestamp.replace(minute=0, second=0, microsecond=0)
        other_hour = hour_timestamp.replace(hour=15)
        energy_detail = EnergyDetails.objects.create(charging_session=self.session_1, timestamp=precise_timestamp, energy=4.4)
        _ = SpotPrices.objects.create(start_time=other_hour, end_time=hour_timestamp.replace(hour=11), **{self.price_area_name: 0.4})

        with self.assertRaises(SpotPrices.DoesNotExist):
            energy_detail.set_spot_price()

    def test_calculate_total_cost_by_filtered_user(self):
        """Test the calculate_total_cost_by_user aggregation function. Using user_id-filter."""
        for energy_detail in self.energy_details:
            energy_detail.set_cost()
            energy_detail.save()

        cost_by_user_1 = EnergyDetails.objects.calculate_total_cost_by_user(user_id=self.user_id_1)[0]
        cost_by_user_2 = EnergyDetails.objects.calculate_total_cost_by_user(user_id=self.user_id_2)[0]

        self.assertEqual(cost_by_user_1["total_energy"], self.energy_detail_1.energy)
        self.assertEqual(cost_by_user_1["total_cost"], self.energy_detail_1.energy * self.spot_price_1.no1)
        self.assertEqual(cost_by_user_1["user_full_name"], self.session_1.user_full_name)
        self.assertEqual(cost_by_user_1["charging_session__user_id"], self.session_1.user_id)

        self.assertEqual(float(cost_by_user_2["total_energy"]), self.energy_detail_2.energy + self.energy_detail_3.energy)
        self.assertAlmostEqual(float(cost_by_user_2["total_cost"]), self.energy_detail_2.cost + self.energy_detail_3.cost, places=6)
        self.assertEqual(cost_by_user_2["user_full_name"], self.session_2.user_full_name)
        self.assertEqual(cost_by_user_2["charging_session__user_id"], self.session_2.user_id)

    def test_calculate_total_cost_by_filtered_time(self):
        """Test the calculate_total_cost_by_user aggregation function. Using time-filter."""
        for energy_detail in self.energy_details:
            energy_detail.set_cost()
            energy_detail.save()

        cost_by_date_2 = EnergyDetails.objects.calculate_total_cost_by_user(start_date=self.datetime_2, end_date=self.datetime_2)[0]

        self.assertEqual(float(cost_by_date_2["total_energy"]), self.energy_detail_2.energy)
        self.assertAlmostEqual(float(cost_by_date_2["total_cost"]), self.energy_detail_2.cost, places=6)
        self.assertEqual(cost_by_date_2["user_full_name"], self.session_2.user_full_name)
        self.assertEqual(cost_by_date_2["charging_session__user_id"], self.session_2.user_id)
