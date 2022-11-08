from rest_framework import serializers

class EmployeeSerializer(serializers.Serializer):
    url = serializers.CharField()
    method = serializers.CharField()
    
