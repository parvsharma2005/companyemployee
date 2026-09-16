from django.db import transaction
from rest_framework import serializers

from .models import Employee, EmployeeAccount


# =========================================================
# Employee Serializer
# =========================================================
class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee

        fields = [
            "id",
            "user",
            "department",
            "manager",
            "name",
            "email",
            "phone",
            "address",
            "website",
            "created_at",
            "updated_at",
            "profile_picture",
        ]

        read_only_fields = [
            "id",
            "user",
            "email",
            "phone",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):

        request = self.context.get("request")

        if not request:
            raise serializers.ValidationError(
                "Request context is required."
            )

        if not request.user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication required."
            )

        # Check whether employee already exists
        if self.instance is None:
          if Employee.objects.filter(
            user=request.user
        ).exists():

            raise serializers.ValidationError({
                "user":
                "An employee profile already exists for this account."
            })
        return data

    @transaction.atomic
    def create(self, validated_data):

        request = self.context["request"]

        # Logged-in EmployeeAccount
        account = request.user

        # Automatically take email and phone
        # from EmployeeAccount
        employee = Employee.objects.create(
            user=account,
            email=account.email,
            phone=account.phone,
            **validated_data
        )

        return employee
# =========================================================
# Employee Bulk Serializer
# =========================================================

class EmployeeBulkSerializer(
    EmployeeSerializer
):
    pass


# =========================================================
# Login Serializer
# =========================================================

class LoginSerializer(serializers.Serializer):

    phone = serializers.CharField(
        min_length=10,
        max_length=10
    )

    password = serializers.CharField(
        write_only=True
    )

    # =====================================================
    # LOGIN VALIDATION
    # =====================================================

    def validate(self, data):

        phone = data.get("phone")
        password = data.get("password")

        # -------------------------------------------------
        # Phone validation
        # -------------------------------------------------

        if not phone.isdigit():

            raise serializers.ValidationError({
                "phone":
                "Phone number must contain numbers only."
            })

        # -------------------------------------------------
        # Find account
        # -------------------------------------------------

        try:

            account = EmployeeAccount.objects.get(
                phone=phone
            )

        except EmployeeAccount.DoesNotExist:

            raise serializers.ValidationError(
                "Invalid phone or password."
            )

        # -------------------------------------------------
        # Check password
        # -------------------------------------------------

        if not account.check_password(password):

            raise serializers.ValidationError(
                "Invalid phone or password."
            )

        # -------------------------------------------------
        # Add account to validated data
        # -------------------------------------------------

        data["account"] = account

        return data