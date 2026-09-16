from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):
    employee = serializers.DictField()
    attendance = serializers.DictField()
    leave = serializers.DictField()
    notifications = serializers.DictField()