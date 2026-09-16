from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    receipt_url = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Expense

        fields = [
            "id",
            "employee",
            "employee_name",
            "category",
            "amount",
            "expense_date",
            "description",
            "receipt",
            "receipt_url",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "receipt_url",
            "created_at",
        ]

    def get_receipt_url(self, obj):

        request = self.context.get("request")

        if obj.receipt and request:
            return request.build_absolute_uri(
                obj.receipt.url
            )

        if obj.receipt:
            return obj.receipt.url

        return None

    def validate_amount(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than 0."
            )

        return value