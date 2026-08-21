from rest_framework import serializers
from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'





class EmployeeBulkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = [
            "id",
            "department",
            "name",
            "email",
            "phone",
            "address",
            "website",
            "created_at",
            "updated_at"
        ]        
        