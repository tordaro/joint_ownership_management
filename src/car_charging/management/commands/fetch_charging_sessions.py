import logging
from django.utils.timezone import datetime, make_aware
from django.core.management.base import BaseCommand, CommandParser

import car_charging.zaptec_services as zts

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Load charging sessions and energy details from the Zaptec API."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("start", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="Start date, inclusive (dd-mm-YYYY).")
        parser.add_argument("end", type=lambda d: datetime.strptime(d, "%d-%m-%Y"), help="End date, inclusive (dd-mm-YYYY).")

    def handle(self, *args, **options) -> None:
        start_date = make_aware(options["start"]).date()
        end_date = make_aware(options["end"]).date()

        if end_date < start_date:
            print("End date must be later than or equal to start date.")
        else:
            charging_data = zts.get_charge_history_data(start_date, end_date)
            _ = zts.create_charging_sessions(charging_data)
