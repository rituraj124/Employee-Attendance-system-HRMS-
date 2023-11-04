from rest_framework import serializers
from .models import Employee,Attandance

class Employeeserializers(serializers.ModelSerializer):
    class Meta:
          model=Employee
          fields="__ALL__"

class Attandaceserializers(serializers.ModelSerializer):
    class Meta:
         model=Attandance
         fields="__ALL__"