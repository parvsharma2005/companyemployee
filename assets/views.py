from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Asset
from .serializers import AssetSerializer


class AssetViewSet(viewsets.ModelViewSet):

    queryset = Asset.objects.select_related(
        "company",
        "assigned_employee"
    ).all()

    serializer_class = AssetSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        company_id = self.request.query_params.get(
            "company"
        )

        employee_id = self.request.query_params.get(
            "employee"
        )

        status = self.request.query_params.get(
            "status"
        )

        category = self.request.query_params.get(
            "category"
        )

        if company_id:
            queryset = queryset.filter(
                company_id=company_id
            )

        if employee_id:
            queryset = queryset.filter(
                assigned_employee_id=employee_id
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if category:
            queryset = queryset.filter(
                category__icontains=category
            )

        return queryset