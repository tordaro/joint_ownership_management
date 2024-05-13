from django.contrib import admin
from car_charging.models import ChargingSession, EnergyDetails, SpotPrice, CostDetails, GridPrice, UsagePrice


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
    list_display = ("id", "nok_pr_kwh", "price_area", "start_time")
    list_filter = ("start_time", "created_at")


class GridPriceAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("id", "day_fee", "night_fee", "day_hour_from", "night_hour_from", "start_date", "created_at")
    list_filter = ("start_date",)


class UsagePriceAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at")
    list_display = ("id", "nok_pr_kwh", "start_date", "created_at")
    list_filter = ("start_date",)


class CostDetailsAdmin(admin.ModelAdmin):
    readonly_fields = (
        "energy",
        "timestamp",
        "price_area",
        "spot_price_nok",
        "grid_price_nok",
        "usage_price_nok",
        "spot_cost",
        "grid_cost",
        "usage_cost",
        "total_cost",
        "user_full_name",
        "user_id",
        "created_at",
        "updated_at",
    )
    list_display = ("energy_detail", "energy", "timestamp", "spot_cost", "grid_cost", "usage_cost", "total_cost", "user_full_name")
    list_filter = ("timestamp", "user_full_name", "user_id")


admin.site.register(ChargingSession, ChargingSessionAdmin)
admin.site.register(EnergyDetails, EnergyDetailsAdmin)
admin.site.register(SpotPrice, SpotPricesAdmin)
admin.site.register(CostDetails, CostDetailsAdmin)
admin.site.register(GridPrice, GridPriceAdmin)
admin.site.register(UsagePrice, UsagePriceAdmin)
