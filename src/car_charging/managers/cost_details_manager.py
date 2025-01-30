from datetime import datetime
from django.db import models
from django.db.models import DecimalField, F, QuerySet, ExpressionWrapper, When, DecimalField, Value, Case
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models.aggregates import Min, Sum, Max, Count


class CostDetailsQuerySet(models.QuerySet):
    def filter_by_user(self, user_id=None, user_full_name=None) -> QuerySet:
        """Optionally filter by user ID or name."""
        queryset = self
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if user_full_name:
            queryset = queryset.filter(user_full_name__icontains=user_full_name)
        return queryset

    def filter_by_date(self, from_date=None, to_date=None) -> QuerySet:
        """Optionally filter by date range."""
        queryset = self
        if from_date:
            queryset = queryset.filter(timestamp__gte=from_date)
        if to_date:
            queryset = queryset.filter(timestamp__lt=to_date)
        return queryset


class CostDetailsManager(models.Manager):

    _aggregations = {
        "energy": Sum("energy"),
        "spot_cost": Sum("spot_cost"),
        "grid_cost": Sum("grid_cost"),
        "usage_cost": Sum("usage_cost"),
        "fund_cost": Sum("fund_cost"),
        "refund": Sum("refund"),
        "total_cost": Sum("total_cost"),
        "cost_pr_kwh": ExpressionWrapper(
            Case(When(energy__gt=0, then=F("total_cost") / F("energy")), default=Value(0), output_field=DecimalField()), output_field=DecimalField()
        ),
        "charging_sessions": Count("session_id", distinct=True),
        "min_timestamp": Min("timestamp"),
        "max_timestamp": Max("timestamp"),
    }

    def get_queryset(self):
        return CostDetailsQuerySet(self.model, using=self._db)

    def filter_by_user(self, user_id=None, user_full_name=None):
        return self.get_queryset().filter_by_user(user_id, user_full_name)

    def filter_by_date(self, from_date=None, to_date=None):
        """Expose filters for direct use."""
        return self.get_queryset().filter_by_date(from_date, to_date)

    def costs_by_user(
        self, user_id: str | None = None, user_full_name: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[dict]:
        """Calculate the total cost by each user and month within a time range."""
        queryset = (
            self.get_queryset()
            .filter_by_user(user_id, user_full_name)
            .filter_by_date(from_date, to_date)
            .annotate(month=TruncMonth("timestamp"), year=TruncYear("timestamp"))
            .values("user_id")
            .annotate(user=Max("user_full_name"), **self._aggregations)
            .order_by("user")
        )
        return list(queryset)

    def costs_by_month(
        self, user_id: str | None = None, user_full_name: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[dict]:
        """Calculate the total cost by each user and month within a time range."""
        queryset = (
            self.get_queryset.filter_by_user(user_id, user_full_name)
            .filter_by_date(from_date, to_date)
            .annotate(month=TruncMonth("timestamp"), year=TruncYear("timestamp"))
            .values("year", "month")
            .annotate(**self._aggregations)
            .order_by("year", "month")
        )
        return list(queryset)

    def costs_by_month_user(
        self, user_id: str | None = None, user_full_name: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[dict]:
        """Calculate the total cost by each user and month within a time range."""
        queryset = (
            self.get_queryset()
            .filter_by_user(user_id, user_full_name)
            .filter_by_date(from_date, to_date)
            .annotate(month=TruncMonth("timestamp"), year=TruncYear("timestamp"))
            .values("user_id", "year", "month")
            .annotate(user=Max("user_full_name"), **self._aggregations)
            .order_by("user", "year", "month")
        )
        return list(queryset)
