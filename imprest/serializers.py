from rest_framework import serializers

from .models import ImprestRequest


class ImprestRequestSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    class Meta:
        model = ImprestRequest

        fields = [
            "id",
            "employee",
            "employee_name",
            "amount",
            "purpose",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "created_at",
        ]

    def validate_amount(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than 0."
            )

        return value

    def validate_purpose(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Purpose cannot be empty."
            )

        return value