from datetime import datetime
from django.db import models
from django.db.models.aggregates import Sum, Max


class EnergyDetailsManager(models.Manager):
    def calculate_total_energy_by_user(
        self, user_id: str | None = None, start_date: datetime | None = None, end_date: datetime | None = None
    ) -> list[dict]:
        """Calculate the total cost by each user within a time range."""
        queryset = self.get_queryset()

        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)

        queryset = queryset.select_related("charging_session")
        if user_id:
            queryset = queryset.filter(charging_session__user_id=user_id)

        total_energy = queryset.values("charging_session__user_id").annotate(
            total_energy=Sum("energy"), user_full_name=Max("charging_session__user_full_name"), user_email=Max("charging_session__user_email")
        )

        return list(total_energy)
