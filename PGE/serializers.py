from rest_framework import serializers

from PGE.models import Employee, Priority, Role


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('magnitude',)

class EmployeeSerializer(serializers.ModelSerializer):
    
    priority = PrioritySerializer(read_only=True, many=True)
    
    class Meta:
        model = Employee
        fields = ('name', 'email', 'priority',)