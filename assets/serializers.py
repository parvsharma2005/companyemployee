from rest_framework import serializers

from .models import Asset


class AssetSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    employee_name = serializers.CharField(
        source="assigned_employee.name",
        read_only=True
    )

    class Meta:
        model = Asset

        fields = [
            "id",
            "company",
            "company_name",
            "asset_name",
            "asset_code",
            "category",
            "assigned_employee",
            "employee_name",
            "assigned_date",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "company_name",
            "employee_name",
            "created_at",
        ]

    def validate(self, data):

        status = data.get(
            "status",
            getattr(self.instance, "status", "available")
        )

        employee = data.get(
            "assigned_employee",
            getattr(
                self.instance,
                "assigned_employee",
                None
            )
        )

        assigned_date = data.get(
            "assigned_date",
            getattr(
                self.instance,
                "assigned_date",
                None
            )
        )

        if status == "assigned":

            if not employee:
                raise serializers.ValidationError({
                    "assigned_employee":
                    "Employee is required when asset is assigned."
                })

            if not assigned_date:
                raise serializers.ValidationError({
                    "assigned_date":
                    "Assigned date is required when asset is assigned."
                })

        return data