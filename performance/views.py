from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import PerformanceReview, Award
from .serializers import (
    PerformanceReviewSerializer,
    AwardSerializer,
)


class PerformanceReviewViewSet(viewsets.ModelViewSet):

    queryset = PerformanceReview.objects.select_related(
        "employee",
        "reviewer",
    ).all()

    serializer_class = PerformanceReviewSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get(
            "employee"
        )

        reviewer_id = self.request.query_params.get(
            "reviewer"
        )

        period = self.request.query_params.get(
            "period"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if reviewer_id:
            queryset = queryset.filter(
                reviewer_id=reviewer_id
            )

        if period:
            queryset = queryset.filter(
                period__icontains=period
            )

        return queryset


class AwardViewSet(viewsets.ModelViewSet):

    queryset = Award.objects.select_related(
        "employee"
    ).all()

    serializer_class = AwardSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get(
            "employee"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        return queryset