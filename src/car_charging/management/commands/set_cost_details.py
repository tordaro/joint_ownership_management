from django.utils.timezone import datetime, make_aware
from django.core.management.base import BaseCommand, CommandParser

from car_charging.cost_services import create_cost_details


class Command(BaseCommand):
    help = "Set cost details."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-s", "--start-date", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="Start date, inclusive (dd-mm-YYYY).")
        parser.add_argument("-e", "--end-date", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="End date, inclusive (dd-mm-YYYY).")

    def handle(self, *args, **options) -> None:
        start_date = None
        end_date = None
        if "start-date" in options:
            start_date = make_aware(options["start-date"])
        if "end-date" in options:
            end_date = make_aware(options["end-date"])

        if start_date and end_date:
            if end_date < start_date:
                print("End date must be later than or equal to start date.")
        else:
            create_cost_details(from_date=start_date, to_date=end_date)
