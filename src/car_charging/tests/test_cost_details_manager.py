import uuid
from django.utils.timezone import datetime, make_aware
from django.test import TestCase
from decimal import Decimal
from car_charging.models import EnergyDetails, GridPrice, SpotPrice, SpotPriceRefund, UsagePrice, CostDetails, ChargingSession


class CostDetailsManagerTestCase(TestCase):
    """Unit tests for the filters and aggregations in the cost details manager."""

    def setUp(self):
        self.datetime_1 = make_aware(datetime(2025, 1, 1, 10))
        self.datetime_2 = make_aware(datetime(2025, 3, 1, 15))
        self.datetime_3 = make_aware(datetime(2025, 4, 1, 10))
        self.datetime_4 = make_aware(datetime(2025, 9, 1, 18))

        self.session_alice = ChargingSession.objects.create(
            user_full_name="Alice",  # relevant field
            user_id=uuid.uuid4(),  # relevant field
            session_id=uuid.uuid4(),
            charger_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            start_date_time=self.datetime_1,
            end_date_time=self.datetime_2,
            price_area=4,
            energy=2.31,
        )
        self.session_bert = ChargingSession.objects.create(
            user_full_name="Bert",  # relevant field
            user_id=uuid.uuid4(),  # relevant field
            session_id=uuid.uuid4(),
            charger_id=uuid.uuid4(),
            device_id=uuid.uuid4(),
            start_date_time=self.datetime_3,
            end_date_time=self.datetime_4,
            price_area=4,
            energy=2.31,
        )
        self.grid_price = GridPrice.objects.create(
            day_fee=Decimal("0.50"),
            night_fee=Decimal("0.30"),
            day_hour_from=6,
            night_hour_from=22,
            start_date=self.datetime_1.date(),
        )
        self.usage_price = UsagePrice.objects.create(
            nok_pr_kwh=Decimal("0.40"),
            start_date=self.datetime_1.date(),
        )
        self.spot_price_refund = SpotPriceRefund.objects.create(
            deduction_threshold=Decimal("0.35"),
            reduction_factor=Decimal("0.1"),
            start_date=self.datetime_1.date(),
        )
        self.spot_price_1 = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("0.55"),
            start_time=self.datetime_1,
            price_area=4,
        )
        self.spot_price_2 = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("0.49"),
            start_time=self.datetime_2,
            price_area=4,
        )
        self.spot_price_3 = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("1.11"),
            start_time=self.datetime_3,
            price_area=4,
        )
        self.spot_price_4 = SpotPrice.objects.create(
            nok_pr_kwh=Decimal("0.67"),
            start_time=self.datetime_4,
            price_area=4,
        )
        self.energy_details_1 = EnergyDetails.objects.create(
            charging_session=self.session_alice,
            energy=Decimal("15.2"),
            timestamp=self.datetime_1,
        )
        self.energy_details_2 = EnergyDetails.objects.create(
            charging_session=self.session_bert,
            energy=Decimal("21.8"),
            timestamp=self.datetime_2,
        )
        self.energy_details_3 = EnergyDetails.objects.create(
            charging_session=self.session_alice,
            energy=Decimal("32.7"),
            timestamp=self.datetime_3,
        )
        self.energy_details_4 = EnergyDetails.objects.create(
            charging_session=self.session_bert,
            energy=Decimal("12.4"),
            timestamp=self.datetime_4,
        )

        CostDetails.objects.create(
            energy_detail=self.energy_details_1,
            spot_price=self.spot_price_1,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )
        CostDetails.objects.create(
            energy_detail=self.energy_details_2,
            spot_price=self.spot_price_2,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )
        CostDetails.objects.create(
            energy_detail=self.energy_details_3,
            spot_price=self.spot_price_3,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )
        CostDetails.objects.create(
            energy_detail=self.energy_details_4,
            spot_price=self.spot_price_4,
            grid_price=self.grid_price,
            usage_price=self.usage_price,
            spot_price_refund=self.spot_price_refund,
        )

    def test_name_filter(self):
        user_full_name = "Alice"
        cost_details = CostDetails.objects.filter_by_user(user_full_name=user_full_name)

        self.assertEqual(len(cost_details), 2)
        self.assertEqual(cost_details[0].energy_detail.charging_session.user_full_name, user_full_name)
        self.assertEqual(cost_details[1].energy_detail.charging_session.user_full_name, user_full_name)

    def test_user_id_filter(self):
        user_id = self.session_bert.user_id
        cost_details = CostDetails.objects.filter_by_user(user_id=user_id)

        self.assertEqual(len(cost_details), 2)
        self.assertEqual(cost_details[0].energy_detail.charging_session.user_id, user_id)
        self.assertEqual(cost_details[1].energy_detail.charging_session.user_id, user_id)

    def test_date_filter(self):
        from_date = self.datetime_2
        to_date = self.datetime_3
        cost_details = CostDetails.objects.filter_by_date(from_date=from_date, to_date=to_date)

        self.assertEqual(len(cost_details), 1)
        self.assertEqual(cost_details[0].energy_detail.timestamp.date(), from_date.date())

    def test_cost_by_user(self):
        user_full_name = "Alice"
        cost_details = CostDetails.objects.filter(energy_detail__charging_session__user_full_name__icontains=user_full_name)
        sum_energy = sum([cost_detail.energy for cost_detail in cost_details])
        sum_spot_cost = sum([cost_detail.spot_cost for cost_detail in cost_details])
        sum_grid_cost = sum([cost_detail.grid_cost for cost_detail in cost_details])
        sum_usage_cost = sum([cost_detail.usage_cost for cost_detail in cost_details])
        sum_fund_cost = sum([cost_detail.fund_cost for cost_detail in cost_details])
        sum_refund = sum([cost_detail.refund for cost_detail in cost_details])
        sum_total_cost = sum([cost_detail.total_cost for cost_detail in cost_details])
        cost_pr_kwh = sum_total_cost / sum_energy
        num_sessions = len({cost_detail.session_id for cost_detail in cost_details})
        min_timestamp = min([cost_detail.timestamp for cost_detail in cost_details])
        max_timestamp = max([cost_detail.timestamp for cost_detail in cost_details])

        result = CostDetails.objects.costs_by_user(user_full_name=user_full_name)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["user"], user_full_name)
        self.assertEqual(result[0]["energy"], sum_energy)
        self.assertEqual(result[0]["spot_cost"], sum_spot_cost)
        self.assertEqual(result[0]["grid_cost"], sum_grid_cost)
        self.assertEqual(result[0]["usage_cost"], sum_usage_cost)
        self.assertEqual(result[0]["fund_cost"], sum_fund_cost)
        self.assertEqual(result[0]["refund"], sum_refund)
        self.assertEqual(result[0]["total_cost"], sum_total_cost)
        self.assertAlmostEqual(result[0]["cost_pr_kwh"], cost_pr_kwh, places=6)
        self.assertEqual(result[0]["charging_sessions"], num_sessions)
        self.assertEqual(result[0]["min_timestamp"], min_timestamp)
        self.assertEqual(result[0]["max_timestamp"], max_timestamp)
