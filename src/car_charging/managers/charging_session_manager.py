from django.db.models.query import QuerySet
from django.db import models


class ChargingSessionManager(models.Manager):
    def get_unique_users(self) -> list[dict[str, str | float | None]]:
        """Return a list of dictionaries with unique user data for each unique user who has charging sessions."""
        users_data: QuerySet = (
            self.get_queryset().order_by("user_id").distinct("user_id").values("user_id", "user_full_name", "user_name", "user_email")
        )
        return list(users_data)
