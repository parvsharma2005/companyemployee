from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

from .models import EmployeeDocument
from .serializers import EmployeeDocumentSerializer


class EmployeeDocumentViewSet(viewsets.ModelViewSet):

    queryset = EmployeeDocument.objects.select_related(
        "employee"
    ).all()

    serializer_class = EmployeeDocumentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):

        queryset = super().get_queryset()

        employee_id = self.request.query_params.get(
            "employee"
        )

        document_type = self.request.query_params.get(
            "document_type"
        )

        if employee_id:
            queryset = queryset.filter(
                employee_id=employee_id
            )

        if document_type:
            queryset = queryset.filter(
                document_type=document_type
            )

        return queryset