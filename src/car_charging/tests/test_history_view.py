import uuid
import pytz
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import datetime
from unittest.mock import patch
from car_charging.views.history import get_charge_history_data, create_charging_sessions, convert_datetime, charge_history
from car_charging.models import ZaptecToken, ChargingSession, EnergyDetails
from car_charging.forms import DateRangeForm


class TestChargingHistoryView(TestCase):
    def setUp(self):
        self.client = Client()

        self.charger_id = uuid.uuid4()
        self.device_id = uuid.uuid4()
        self.session_id = uuid.uuid4()
        self.user_id = uuid.uuid4()
        self.data = [
            {
                "ChargerId": str(self.charger_id),
                "CommitEndDateTime": "2022-01-01T00:00:00",
                "CommitMetadata": 5,
                "DeviceId": str(self.device_id),
                "DeviceName": "test_device_name",
                "EndDateTime": "2022-01-01T00:00:00",
                "Energy": 100.000,
                "ExternallyEnded": False,
                "Id": str(self.session_id),
                "StartDateTime": "2022-01-01T00:00:00",
                "UserEmail": "test@example.com",
                "UserFullName": "Test User",
                "UserId": str(self.user_id),
                "UserName": "test_user",
                "EnergyDetails": [
                    {
                        "Energy": 50,
                        "Timestamp": "2022-01-01T00:00:00+00:00",
                    },
                    {
                        "Energy": 50,
                        "Timestamp": "2022-01-01T00:30:00+00:00",
                    },
                ],
            },
        ]
        self.zaptec_token = ZaptecToken.objects.create(
            token="test_token",
            expires_in=60 * 60 * 24,
        )

    def test_create_charging_sessions(self):
        result = create_charging_sessions(self.data)

        session = result[0]
        self.assertEqual(len(result), 1)
        self.assertEqual(session.charger_id, str(self.charger_id))
        self.assertEqual(session.commit_metadata, 5)
        self.assertEqual(session.device_id, str(self.device_id))
        self.assertEqual(session.device_name, "test_device_name")
        self.assertEqual(session.energy, 100.000)
        self.assertEqual(session.externally_ended, False)
        self.assertEqual(session.session_id, str(self.session_id))
        self.assertEqual(session.user_email, "test@example.com")
        self.assertEqual(session.user_full_name, "Test User")
        self.assertEqual(session.user_id, str(self.user_id))
        self.assertEqual(session.user_name, "test_user")
        self.assertEqual(session.energydetails_set.count(), 2)

    def test_charge_history_get(self):
        client = Client()
        response = client.get(reverse("charging:history"))
        self.assertEqual(response.status_code, 200)

    @patch("car_charging.views.history.get_charge_history_data")
    def test_charge_history_post(self, mock_get_charge_history_data):
        mock_get_charge_history_data.return_value = self.data
        form_data = {
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
        }
        response = self.client.post(reverse("charging:history"), data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_convert_datetime_floating_point(self):
        datetime_string = "2022-01-01T00:00:00.00000+00:00"
        expected_result = datetime(2022, 1, 1, tzinfo=pytz.utc)

        result = convert_datetime(datetime_string)

        self.assertEqual(result, expected_result)

    def test_convert_datetime_not_floating_point(self):
        datetime_string = "2022-01-01T00:00:00+00:00"
        expected_result = datetime(2022, 1, 1, tzinfo=pytz.utc)

        result = convert_datetime(datetime_string)

        self.assertEqual(result, expected_result)
