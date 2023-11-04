from django.db import models

# Create your models here.


class Employee(models.Model):
      Empcode=models.CharField(primary_key=True,unique=True,max_length=20)
      Name=models.CharField(max_length=20,blank=True)
    
class Attandance(models.Model):
      employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
      Date=models.DateField(null=True)
      InTime=models.TimeField(null=True)
      OutTime=models.TimeField(null=True)
      WorkingHour=models.TimeField(null=True)
      OverTime=models.TimeField(null=True)
      Status=models.CharField(max_length=10)
      Remark=models.CharField(max_length=20,null=True)
      class Meta:
            unique_together=('employee','Date')
            