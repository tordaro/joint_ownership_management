import logging
from django.core.management.base import BaseCommand, CommandParser

from car_charging.models import SpotPrice

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Convenience command that just returns latest spot price."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("price_area", type=int, help="Price area.")

    def handle(self, *args, **options) -> None:
        price_area = options["price_area"]
        spot_price = SpotPrice.objects.filter(price_area=price_area).first()

        if spot_price:
            print(f"Date: {spot_price.start_time}")
            print(f"Price area: {price_area}")
            print(f"Price [NOK]: {spot_price.nok_pr_kwh}")
