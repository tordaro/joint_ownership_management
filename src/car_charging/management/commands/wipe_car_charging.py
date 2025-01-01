import logging
from django.core.management.base import BaseCommand, CommandParser

from car_charging.models import ChargingSession, CostDetails, EnergyDetails, GridPrice, SpotPrice, SpotPriceRefund, UsagePrice

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = "Wipe all car_charing models, except tokens."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-y", "--yes", action="store_true")

    def handle(self, *args, **options) -> None:
        is_yes = options["yes"]
        if not is_yes:
            is_confirmed = input("Irreversible delete all car charging data? (y/n) ")
            if is_confirmed.lower() != "y":
                print("Aborted.")
                return

        if is_yes or is_confirmed:
            CostDetails.objects.all().delete()
            EnergyDetails.objects.all().delete()
            ChargingSession.objects.all().delete()
            SpotPrice.objects.all().delete()
            GridPrice.objects.all().delete()
            UsagePrice.objects.all().delete()
            SpotPriceRefund.objects.all().delete()
