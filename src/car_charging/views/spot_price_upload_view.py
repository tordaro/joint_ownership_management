from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import csv
from django.utils.dateparse import parse_datetime

from car_charging.models import SpotPrices
from car_charging.forms import CSVUploadForm


class SpotPricesUploadView(View):
    def get(self, request):
        form = CSVUploadForm()
        return render(request, "car_charging/spot_price_upload.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            decoded_file = csv_file.read().decode("utf-8-sig").splitlines()
            reader = csv.DictReader(decoded_file, delimiter=";")

            for row in reader:
                # The date and time are in 'Dato/klokkeslett' column, need to parse and split it
                print(row)
                date_time_str = row["Dato/klokkeslett"].replace(" Kl. ", " ")  # Replace ' Kl. ' with space for parsing
                start_time_str = date_time_str.split("-")[0]  # Split at '-' to get start time
                start_time = parse_datetime(f"{start_time_str}:00")  # Append seconds and parse

                # Prices need to replace commas with dots to convert to float
                prices = {
                    "no1": row["NO1"].replace(",", "."),
                    "no2": row["NO2"].replace(",", "."),
                    "no3": row["NO3"].replace(",", "."),
                    "no4": row["NO4"].replace(",", "."),
                    "no5": row["NO5"].replace(",", "."),
                }

                # Convert string prices to float and handle missing or malformed values
                prices_clean = {k: float(v) if v not in (None, "", "NULL") else None for k, v in prices.items()}

                # Assuming 'start_time' uniquely identifies your SpotPrices instance
                # and the end_time can be calculated or is not critical for the uniqueness
                SpotPrices.objects.update_or_create(
                    start_time=start_time,
                    defaults=prices_clean,
                )
            return HttpResponse("CSV file processed successfully")
        else:
            return HttpResponse("There was an error processing your file")
