import logging
from django.utils.timezone import datetime, make_aware, timedelta
from django.core.management.base import BaseCommand, CommandParser

from car_charging.hks_services import create_daily_spot_prices
from car_charging.models import SpotPrice

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Fetch spot price data from hvakosterstrommen-API in given date range."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("price_area", type=int, choices=range(1, 5), help="Price area.")
        parser.add_argument("start", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="Start date, inclusive (dd-mm-YYYY).")
        parser.add_argument("end", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="End date, inclusive (dd-mm-YYYY).")

    def handle(self, *args, **options) -> None:
        start_date = make_aware(options["start"]).date()
        end_date = make_aware(options["end"]).date()
        price_area = options["price_area"]
        control_date = start_date

        if end_date < start_date:
            print("End date must be later than or equal to start date.")
        else:
            while control_date <= end_date:
                spot_price_count = SpotPrice.objects.filter(start_time__date=control_date).count()

                if spot_price_count != 24:
                    create_daily_spot_prices(control_date, price_area=price_area)

                control_date += timedelta(days=1)
