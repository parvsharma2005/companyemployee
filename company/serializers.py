from rest_framework import serializers
from .models import *


class companySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = '__all__'