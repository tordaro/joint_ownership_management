from datetime import datetime
from django.db import models
from django.db.models import DecimalField, F, QuerySet
from django.db.models import ExpressionWrapper
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models.aggregates import Min, Sum, Max, Count


class CostDetailsManager(models.Manager):

    _aggregations = {
        "energy": Sum("energy"),
        "spot_cost": Sum("spot_cost"),
        "grid_cost": Sum("grid_cost"),
        "usage_cost": Sum("usage_cost"),
        "fund_cost": Sum("fund_cost"),
        "refund": Sum("refund"),
        "total_cost": Sum("total_cost"),
        "cost_pr_kwh": ExpressionWrapper(F("total_cost") / F("energy"), output_field=DecimalField()),
        "charging_sessions": Count("session_id", distinct=True),
        "min_timestamp": Min("timestamp"),
        "max_timestamp": Max("timestamp"),
    }

    def _add_filters(
        self,
        queryset: QuerySet,
        user_id: str | None = None,
        user_full_name: str | None = None,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> QuerySet:
        if from_date:
            queryset = queryset.filter(timestamp__gte=from_date)
        if to_date:
            queryset = queryset.filter(timestamp__lt=to_date)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if user_full_name:
            queryset = queryset.filter(user_full_name__icontains=user_full_name)
        return queryset

    def costs_by_user(
        self, user_id: str | None = None, user_full_name: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[dict]:
        """Calculate the total cost by each user and month within a time range."""
        queryset = self.get_queryset()
        queryset = self._add_filters(queryset, user_id, user_full_name, from_date, to_date)
        queryset = (
            queryset.annotate(month=TruncMonth("timestamp"), year=TruncYear("timestamp"))
            .values("user_id")
            .annotate(user=Max("user_full_name"), **self._aggregations)
            .order_by("user")
        )
        return list(queryset)

    def costs_by_month(
        self, user_id: str | None = None, user_full_name: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[dict]:
        """Calculate the total cost by each user and month within a time range."""
        queryset = self.get_queryset()
        queryset = self._add_filters(queryset, user_id, user_full_name, from_date, to_date)
        queryset = (
            queryset.annotate(month=TruncMonth("timestamp"), year=TruncYear("timestamp"))
            .values("month", "year")
            .annotate(**self._aggregations)
            .order_by("year", "month")
        )
        return list(queryset)

    def costs_by_month_user(
        self, user_id: str | None = None, user_full_name: str | None = None, from_date: datetime | None = None, to_date: datetime | None = None
    ) -> list[dict]:
        """Calculate the total cost by each user and month within a time range."""
        queryset = self.get_queryset()
        queryset = self._add_filters(queryset, user_id, user_full_name, from_date, to_date)
        queryset = (
            queryset.annotate(month=TruncMonth("timestamp"), year=TruncYear("timestamp"))
            .values("user_id", "month", "year")
            .annotate(user=Max("user_full_name"), **self._aggregations)
            .order_by("user", "year", "month")
        )
        return list(queryset)
