import openpyxl as xl
from pathlib import Path
from django.utils.timezone import datetime, make_aware

from car_charging.models.SpotPrice import SpotPrice


def parse_datetime(datetime_str: str) -> datetime:
    date_part, time_part = datetime_str.split(" Kl. ")
    hour_str = time_part.split("-")[0].strip()
    new_datetime_str = f"{date_part} {hour_str}"
    parsed_datetime = datetime.strptime(new_datetime_str, "%Y-%m-%d %H")
    return parsed_datetime


def load_spot_prices(file_path: Path) -> None:
    workbook = xl.load_workbook(file_path)
    sheet = workbook.worksheets[0]
    rows = list(sheet.iter_rows(values_only=True))
    spot_prices = []
    for row in rows[1:]:
        for price_area in range(1, 6):
            start_time = make_aware(parse_datetime(row[0]))
            spot_price = SpotPrice(start_time=start_time, nok_per_kwh=row[1], price_area=price_area)
            spot_prices.append(spot_price)

    SpotPrice.objects.bulk_create(spot_prices)
