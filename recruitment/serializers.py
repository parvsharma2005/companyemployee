from rest_framework import serializers

from .models import JobOpening


class JobOpeningSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    department_name = serializers.CharField(
        source="department.name",
        read_only=True
    )

    class Meta:
        model = JobOpening

        fields = [
            "id",
            "company",
            "company_name",
            "department",
            "department_name",
            "title",
            "description",
            "vacancies",
            "location",
            "opening_date",
            "closing_date",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "company_name",
            "department_name",
            "created_at",
        ]

    def validate_vacancies(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Vacancies must be greater than 0."
            )

        return value

    def validate_title(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Job title cannot be empty."
            )

        return value

    def validate_description(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Job description cannot be empty."
            )

        return value

    def validate_location(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Location cannot be empty."
            )

        return value

    def validate(self, attrs):

        opening_date = attrs.get("opening_date")
        closing_date = attrs.get("closing_date")

        if (
            opening_date
            and closing_date
            and closing_date < opening_date
        ):
            raise serializers.ValidationError({
                "closing_date":
                    "Closing date cannot be before opening date."
            })

        return attrs