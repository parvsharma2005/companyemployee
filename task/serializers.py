from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    employee_name = serializers.CharField(
        source="employee.name",
        read_only=True
    )

    class Meta:
        model = Task

        fields = [
            "id",
            "employee",
            "employee_name",
            "title",
            "description",
            "start_date",
            "due_date",
            "status",
            "priority",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "employee_name",
            "created_at",
        ]

    def validate(self, data):

        start_date = data.get("start_date")
        due_date = data.get("due_date")

        if (
            start_date
            and due_date
            and due_date < start_date
        ):
            raise serializers.ValidationError({
                "due_date":
                    "Due date cannot be before start date."
            })

        return data