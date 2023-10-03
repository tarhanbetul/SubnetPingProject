from rest_framework import serializers
from .models import Subnet

class SubnetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subnet
        fields = '__all__'


class PingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = PingResult
        fields = '__all__'