from tabulate import tabulate
from django.utils.timezone import datetime, make_aware
from django.core.management.base import BaseCommand, CommandParser

from car_charging.models import CostDetails


class Command(BaseCommand):
    help = "Print cost details aggregates."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-s", "--start-date", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="Start date, inclusive (dd-mm-YYYY).")
        parser.add_argument("-e", "--end-date", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="End date, inclusive (dd-mm-YYYY).")
        parser.add_argument("-u", "--user-id", type=str, help="Filter by user ID.")
        parser.add_argument("-n", "--user-name", type=str, help="Filter by part of user name. Case insensitive.")
        parser.add_argument("by", choices=["month", "user", "user-month"])

    def handle(self, *args, **options) -> None:
        filters = {
            "from_date": options.get("start-date", None),
            "to_date": options.get("end_date", None),
            "user_id": options.get("user_id", None),
            "user_full_name": options.get("user_name", None),
        }

        if options["by"] == "month":
            data = CostDetails.objects.costs_by_month(**filters)
            for row in data:
                row["year"] = row["year"].year
                row["month"] = row["month"].month
                row["min_timestamp"] = row["min_timestamp"].date()
                row["max_timestamp"] = row["max_timestamp"].date()
        elif options["by"] == "user":
            data = CostDetails.objects.costs_by_user(**filters)
            for row in data:
                row["min_timestamp"] = row["min_timestamp"].date()
                row["max_timestamp"] = row["max_timestamp"].date()
        elif options["by"] == "user-month":
            data = CostDetails.objects.costs_by_month_user(**filters)
            for row in data:
                row["year"] = row["year"].year
                row["month"] = row["month"].month
                row["min_timestamp"] = row["min_timestamp"].date()
                row["max_timestamp"] = row["max_timestamp"].date()

        print(tabulate(data, headers="keys"))
