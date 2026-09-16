from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import JobOpening
from .serializers import JobOpeningSerializer


class JobOpeningViewSet(viewsets.ModelViewSet):

    queryset = JobOpening.objects.select_related(
        "company",
        "department",
    ).all()

    serializer_class = JobOpeningSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        company_id = self.request.query_params.get(
            "company"
        )

        department_id = self.request.query_params.get(
            "department"
        )

        status = self.request.query_params.get(
            "status"
        )

        location = self.request.query_params.get(
            "location"
        )

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if department_id:
            queryset = queryset.filter(
                department_id=department_id
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        return queryset