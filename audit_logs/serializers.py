from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "action",
            "module",
            "object_id",
            "description",
            "old_data",
            "new_data",
            "ip_address",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "ip_address",
            "created_at",
        ]