from django.contrib import admin
from car_charging.models import ChargingSession, EnergyDetails

class ChargingSessionAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_email', 'start_date_time', 'energy', 'device_name', 'created_at')
    list_filter = ('user_full_name', 'user_name', 'user_email', 'start_date_time', 'end_date_time', 'energy', 'device_name', 'created_at')
    search_fields = ('user_full_name', "user_name")

class EnergyDetailsAdmin(admin.ModelAdmin):
    list_display = ('charging_session', 'energy', 'timestamp', 'created_at')
    list_filter = ('charging_session', 'energy', 'timestamp', 'created_at')
    search_fields = ('charging_session',)

admin.site.register(ChargingSession, ChargingSessionAdmin)
admin.site.register(EnergyDetails, EnergyDetailsAdmin)