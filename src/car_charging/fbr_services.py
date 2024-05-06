import logging
import openpyxl as xl
from pathlib import Path
from django.utils.timezone import datetime, make_aware

from car_charging.models.SpotPrice import SpotPrice

logger = logging.getLogger("django")


def parse_datetime(datetime_str: str) -> datetime:
    date_part, time_part = datetime_str.split(" Kl. ")
    hour_str = time_part.split("-")[0].strip()
    new_datetime_str = f"{date_part} {hour_str}"
    parsed_datetime = datetime.strptime(new_datetime_str, "%Y-%m-%d %H")
    return make_aware(parsed_datetime)


def load_spot_prices(file_path: Path) -> None:
    workbook = xl.load_workbook(file_path)
    sheet = workbook.worksheets[0]
    rows = list(sheet.iter_rows(values_only=True))
    spot_prices = []
    for row in rows[1:]:
        for i in range(1, 6):
            start_time = parse_datetime(row[0])  # type: ignore
            nok_pr_kwh = str(row[i]).replace(",", ".")
            spot_price = SpotPrice(start_time=start_time, price_area=i, nok_pr_kwh=nok_pr_kwh)
            spot_prices.append(spot_price)
            logger.info(f"Adding spot price for {spot_price.start_time} price area {spot_price.price_area}.")

    SpotPrice.objects.bulk_create(spot_prices)
    logger.info(f"Inserted {len(spot_prices)} spot prices.")
