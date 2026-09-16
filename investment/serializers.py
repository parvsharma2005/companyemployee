from rest_framework import serializers

from .models import InvestmentDeclaration


class InvestmentDeclarationSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    class Meta:
        model = InvestmentDeclaration

        fields = [
            "id",
            "employee",
            "employee_name",
            "financial_year",
            "investment_type",
            "amount",
            "document",
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

    def validate_financial_year(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Financial year cannot be empty."
            )

        return value

    def validate_investment_type(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Investment type cannot be empty."
            )

        return value