from django.apps import AppConfig


class CarChargingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "car_charging"

    def ready(self):
        import car_charging.signals
