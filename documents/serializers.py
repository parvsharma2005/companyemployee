from rest_framework import serializers

from .models import EmployeeDocument


class EmployeeDocumentSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    file_url = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = EmployeeDocument

        fields = [
            "id",
            "employee",
            "employee_name",
            "document_type",
            "document_name",
            "file",
            "file_url",
            "uploaded_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "file_url",
            "uploaded_at",
        ]

    def get_file_url(self, obj):

        request = self.context.get("request")

        if obj.file and request:
            return request.build_absolute_uri(
                obj.file.url
            )

        if obj.file:
            return obj.file.url

        return None