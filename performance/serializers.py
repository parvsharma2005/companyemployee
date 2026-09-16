from rest_framework import serializers

from .models import PerformanceReview, Award


class PerformanceReviewSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    reviewer_name = serializers.CharField(
        source="reviewer.name",
        read_only=True
    )

    class Meta:
        model = PerformanceReview

        fields = [
            "id",
            "employee",
            "employee_name",
            "reviewer",
            "reviewer_name",
            "rating",
            "comments",
            "review_date",
            "period",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "reviewer_name",
            "created_at",
        ]

    def validate_rating(self, value):

        if value < 0 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 0 and 5."
            )

        return value

    def validate_period(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Period cannot be empty."
            )

        return value


class AwardSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    class Meta:
        model = Award

        fields = [
            "id",
            "employee",
            "employee_name",
            "title",
            "description",
            "awarded_date",
            "awarded_by",
        ]

        read_only_fields = [
            "id",
            "employee_name",
        ]

    def validate_title(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Award title cannot be empty."
            )

        return value