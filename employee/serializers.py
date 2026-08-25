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
        
        
        
class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            account = EmployeeAccount.objects.get(phone=data["phone"])
        except EmployeeAccount.DoesNotExist:
            raise serializers.ValidationError("Invalid phone or password")

        if not account.check_password(data["password"]):
            raise serializers.ValidationError("Invalid phone or password")

        data["account"] = account
        return data        
        