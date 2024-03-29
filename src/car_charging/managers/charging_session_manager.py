from django.db.models.query import QuerySet
from django.db import models
from django.db.models import Prefetch

from car_charging.models.EnergyDetails import EnergyDetails


class ChargingSessionManager(models.Manager):
    def calculate_user_cost(self, user_id, start_date=None, end_date=None) -> float:
        """Calculate the total charging cost for a specific user within a date range."""
        queryset = self.get_queryset()

        if start_date:
            queryset = queryset.filter(start_date_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_date_time__lte=end_date)

        queryset = queryset.filter(user_id=user_id).prefetch_related(
            Prefetch("energydetails_set", queryset=EnergyDetails.objects.all().select_related("spot_price"))
        )

        total_cost = sum([session.calculate_cost() for session in queryset])
        return total_cost

    def get_unique_users(self) -> list[dict[str, str | float | None]]:
        """Return a list of dictionaries with unique user data for each unique user who has charging sessions."""
        users_data: QuerySet = (
            self.get_queryset().order_by("user_id").distinct("user_id").values("user_id", "user_full_name", "user_name", "user_email")
        )
        return list(users_data)

    def calculate_total_cost_by_user(self, start_date=None, end_date=None) -> list[dict[str, str | float | None]]:
        users = self.get_unique_users()
        users_with_cost = []
        for user in users:
            user_with_cost = user.copy()
            user_with_cost["total_cost"] = self.calculate_user_cost(user["user_id"], start_date, end_date)
            users_with_cost.append(user_with_cost)
        return users_with_cost
