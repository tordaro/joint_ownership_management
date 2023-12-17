import unittest
import pytz
from unittest.mock import patch, Mock
from django.utils.timezone import datetime
from urllib3.response import HTTPResponse
from car_charging.views import utils


class TestUtils(unittest.TestCase):
    @patch("urllib3.PoolManager")
    def test_request_charge_history(self, mock_pool_manager):
        mock_response = Mock(spec=HTTPResponse)
        mock_pool_manager.return_value.request.return_value = mock_response

        access_token = "test_token"
        installation_id = "test_id"
        from_date = datetime(2022, 1, 1)
        to_date = datetime(2022, 1, 31)

        response = utils.request_charge_history(access_token, installation_id, from_date, to_date)

        self.assertEqual(response, mock_response)
        mock_pool_manager.return_value.request.assert_called_once_with(
            "GET",
            "https://api.zaptec.com/api/chargehistory",
            headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json-patch+json"},
            fields={
                "InstallationId": installation_id,
                "GroupBy": "2",
                "DetailLevel": "1",
                "From": from_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
                "To": to_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
            },
        )

    def test_convert_datetime_floating_point(self):
        datetime_string = "2022-01-01T00:00:00.00000+00:00"
        expected_result = datetime(2022, 1, 1, tzinfo=pytz.utc)

        result = utils.convert_datetime(datetime_string)

        self.assertEqual(result, expected_result)

    def test_convert_datetime_not_floating_point(self):
        datetime_string = "2022-01-01T00:00:00+00:00"
        expected_result = datetime(2022, 1, 1, tzinfo=pytz.utc)

        result = utils.convert_datetime(datetime_string)

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
