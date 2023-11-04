from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
import datetime
from requests.auth import HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.db import transaction
from .models import Employee,Attandance
import calendar
# Create your views here.


def edt(empid):
         url='https://api.etimeoffice.com/api/DownloadInOutPunchData?Empcode='
         apiurl=f'{url}{empid}'
         response=requests.get(apiurl,auth=HTTPBasicAuth('bariflolabs:admin:BFL0@2022@18:true','BFL0@2022@18'))
         parsed_data=response.json()
         for i in parsed_data['InOutPunchData']:
             empcode=i['Empcode']
             empname=i['Name']
             date=i['DateString']
             date_obj=datetime.datetime.strptime(date, "%d/%m/%Y")
             formatted_date = date_obj.date().strftime("%Y-%m-%d")
             intim=i['INTime']
             if intim != "--:--":
                 intime=datetime.datetime.strptime(intim,"%H:%M").strftime("%H:%M:%S")
             else:
                 intime=None
             outtim=i['OUTTime']
             if outtim != "--:--":
                outtime=datetime.datetime.strptime(outtim,"%H:%M").strftime("%H:%M:%S")
             else:
                 outtime=None
             workinghou=i['WorkTime']
             if workinghou != "--:--":
                workinghour=datetime.datetime.strptime(workinghou,"%H:%M").strftime("%H:%M:%S")
             else:
                 workinghour=None
             overtim=i['OverTime']
             if overtim != "--:--":
                overtime=datetime.datetime.strptime(overtim,"%H:%M").strftime("%H:%M:%S")
             else:
                 overtime=None
             status=i['Status']
             remark=i['Remark']
             try:
                employee=Employee.objects.get(Empcode=empcode)
             except Employee.DoesNotExist:
                employee=Employee.objects.create(Empcode=empcode,Name=empname)
                employee.save()
             try:
                attandence=Attandance.objects.get(employee=employee,Date=formatted_date)
             except Attandance.DoesNotExist:
                attandence=Attandance.objects.create(employee=employee,Date=formatted_date,InTime=intime,OutTime=outtime,WorkingHour=workinghour,OverTime=overtime,Status=status,Remark=remark)
                attandence.save()
@csrf_exempt       
def edttt(empid,date1,date2):
    if empid != 'ALL':
       try:
           employee=Employee.objects.get(Empcode=empid)
       except Employee.DoesNotExist:
           return HttpResponse(f"Employee with employee code {empid} doesnot exist")
       attandance_data=Attandance.objects.filter(employee=employee,Date__range=[date1,date2])
    else:
        attandance_data=Attandance.objects.filter(Date__range=[date1,date2])
    data_list=[]
    for attandance in attandance_data:
        data_list.append({
          'Empcode':attandance.employee.Empcode,
          'Name':attandance.employee.Name,
          'Date':attandance.Date.strftime('%Y-%m-%d'),
          'InTime':attandance.InTime.strftime('%H:%M:%S') if attandance.InTime else None,
          'OutTime':attandance.OutTime.strftime('%H:%M:%S') if attandance.OutTime else None,
          'status':attandance.Status,
        })
    return data_list
def view1():
     edt('ALL')
     
def send_late():
    date=datetime.datetime.today()
    employee=Employee.objects.all()
    late=[]
    present=[]
    absent=[]
    weeklyoff=[]
    for emp in employee:
        attandance=Attandance.objects.filter(employee=emp,Date=date)
        for i in attandance:
            if i.Status == "P" and  i.Remark == "MIS-EI":
                present.append(i.employee.Name)
            elif i.Status == "P" and i.Remark == "MIS-LT":
                late.append(i.employee.Name)
            elif i.Status == "A":
                absent.append(i.employee.Name)
            elif i.Status == "WO":
                weeklyoff.append(i.employee.Name)
    late_str='\n'.join(late)
    present_str='\n'.join(present)
    absent_str="\n".join(absent)
    wo_str='\n'.join(weeklyoff)
    send_mail(
        "Late And Absent Employees" ,#Email subject
        "Hello \n Good Morning. \n Below are the Late Employees For today\n\n"
                                            +late_str+
                            "\n\n Below are the employees Absent Till Now\n\n"
                                            +absent_str+
                              "\n\n Below are the employees Have Weekly OFF Today\n\n"
                                            +wo_str+
                              "\n\n Employees present Today\n\n"
                                           +present_str,#Email Body
         'dasrituraj04@gmail.com',#Sender's Email Address
        ['dasrituraj04@gmail.com']    ,#list of Recipient Employee
        fail_silently=False  # Raise an Exception If Sending Fails
    )
    print('message sent')


def combinedmodel_logic():
    emplyeedata=Employee.objects.all()
    combined_data=[]
    for data1 in emplyeedata:
        try:
            attandancedata=Attandance.objects.get(employee_id=data1,Date=datetime.datetime.today())
            combined_data.append({
                'Empid':data1.Empcode,
                'Name':data1.Name,
                'Date':attandancedata.Date,
                'InTime':attandancedata.InTime,
                'OutTime':attandancedata.OutTime,
                'WorkingHour':attandancedata.WorkingHour,
                'OverTime':attandancedata.OverTime,
                'Status':attandancedata.Status,
                'Remark':attandancedata.Remark
            })
        except Attandance.DoesNotExist :
            print('Employee Data Doesnot Exists')
    return combined_data

@csrf_exempt
def combinedmodel_view(request):
     combineddata=combinedmodel_logic()
     if isinstance(combineddata, HttpResponse):
        # Handle the case where `combinedmodel_logic` returns an HttpResponse object
        return combineddata
    
     return JsonResponse(combineddata, safe=False)

@csrf_exempt
def monthly_data(request):
    a=datetime.datetime.now()
    b=int(a.strftime('%Y'))
    c=int(a.strftime('%m'))
    first,last=calendar.monthrange(b,c)
    date1=datetime.datetime(b,c,1)
    date2=datetime.datetime(b,c,last)
    val=edttt('ALL',date1,date2)
    return JsonResponse(val,safe=False)