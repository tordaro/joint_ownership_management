from django.contrib import admin
from car_charging.models import ChargingSession, EnergyDetails, SpotPrice, Costs, GridPrice


class ChargingSessionAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("id", "user_full_name", "user_email", "start_date_time", "energy", "device_name", "created_at")
    list_filter = ("user_full_name", "user_name", "user_email", "start_date_time", "end_date_time", "energy", "device_name", "created_at")
    search_fields = ("user_full_name", "user_name")


class EnergyDetailsAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("id", "charging_session", "energy", "timestamp", "created_at")
    list_filter = ("charging_session", "energy", "timestamp", "created_at")
    search_fields = ("charging_session",)


class SpotPricesAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("id", "nok_pr_kwh", "eur_pr_kwh", "exchange_rate", "price_area", "start_time")
    list_filter = ("start_time", "created_at")


class CostsAdmin(admin.ModelAdmin):
    readonly_fields = (
        "energy",
        "timestamp",
        "price_area",
        "spot_nok_pr_kwh",
        "grid_nok_pr_kwh",
        "spot_cost",
        "grid_cost",
        "created_at",
        "updated_at",
    )
    list_display = ("energy_detail", "energy", "timestamp", "spot_nok_pr_kwh", "grid_nok_pr_kwh", "spot_cost", "grid_cost")
    list_filter = ("timestamp",)


class GridPriceAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("id", "day_fee", "night_fee", "day_hour_from", "night_hour_from", "start_date", "created_at")
    list_filter = ("start_date",)


admin.site.register(ChargingSession, ChargingSessionAdmin)
admin.site.register(EnergyDetails, EnergyDetailsAdmin)
admin.site.register(SpotPrice, SpotPricesAdmin)
admin.site.register(Costs, CostsAdmin)
admin.site.register(GridPrice, GridPriceAdmin)
