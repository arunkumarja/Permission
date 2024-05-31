from rest_framework.views import APIView
from rest_framework.response import Response 
from .models import *
# from serializers import *
from django.http import JsonResponse
from .serializers import UserSerializer,FileSerializer,BlobModelSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.parsers import FileUploadParser
import pandas as pd
from io import StringIO
from .tasks import *
from django.http import HttpResponse
from sent_mail_app.tasks import send_mail_func,bday_fun
from celery.schedules import crontab


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({"message":serializer.data})  
        

class FileUploadAPI(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=201)
        else:
            return Response(file_serializer.errors, status=400)  

    def get(self,request):
        query=request.query_params.get('id')
        file=FileUpload.objects.get(id=query)
        data=file.upload
        return Response({"data":data})
class BlobModelAPI(APIView):
    parser_class = (MultiPartParser, FormParser)
    def post(self,request):
        file=request.FILES.get('file')
        if file:
            file_content = file.read()        
            blob=BlobModel.objects.create(name='fun',blob=file_content)
            blob.save()
        return Response("success")

    def get(self,request):
        query=request.query_params.get('id') 
        blob=BlobModel.objects.get(id=query)
        data=blob.blob
        return Response({"blob data":data})  


class CSVFileAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self,request,*args,**kwargs):
        try:
            file = request.FILES.get('file')
            print(file)
            if not file:
                return Response({"error": "No file provided"})
            try:
                # df= pd.read_csv(file,encoding='latin1')
                json_data=df.to_dict(orient='records')
            except Exception as e:
                return Response({"error":str(e)})
            # df = pd.read_csv(file, encoding='latin1')    
            data=CSVFile(csv=json_data)   
            data.save()
            return Response({"message": "File successfully uploaded and data saved"})
        except Exception as e:
            return Response({"error":str(e)})      

    # def get(self,request):
    #     query=request.query_params.get('id') 
    #     csv_data=CSVFile.objects.get(id=query)
    #     instance=csv_data.csv 
    #     a=[]  
    #     for i in instance:
    #         total=i['maths']+i['tamil']+i['social']+i['english']+i['science']
    #         i['total']=total 
    #         x=i['total']
    #         a.append(x)
    #     sorted_totals = sorted(a, reverse=True)
    #     for student in instance:
    #         if student['maths']<35 or student['tamil']<35 or student['social']<35 or student['english']<35 or student['science']<35 :
    #             student['rank']='Fail'
    #         else:
    #             student['rank'] = sorted_totals.index(student['total']) +1
    #     return Response(instance) 
     


    def get(self, request, *args, **kwargs):
        # Get the ID from query parameters
        query_id = request.query_params.get('id')
        
        # Fetch the CSV data from the database
        csv_data = CSVFile.objects.get(id=query_id)
        instance = csv_data.csv
        df = pd.DataFrame(instance)
        # Calculate the total scores for each student
        df['total'] = df[['maths', 'tamil', 'social', 'english', 'science']].sum(axis=1) 
        # Determine if a student has failed in any subject
        df['rank'] = df.apply(
            lambda row: 'Fail' if any(row[subject] < 35 for subject in ['maths', 'tamil', 'social', 'english', 'science']) else None,
            axis=1
        )
        df_not_failed = df[df['rank'] != 'Fail']
        df_not_failed = df_not_failed.sort_values(by='total', ascending=False)
        df_not_failed['rank'] = range(1, len(df_not_failed) + 1)
        df.update(df_not_failed['rank'])
        students = df.to_dict(orient='records')
        
        return Response(students)


def test(request):
    add.delay(10)
    return HttpResponse("Done")

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("sent")

from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Students

def schedule_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 11, minute = 57)
    task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_tasks_3", task='sent_mail_app.tasks.send_mail_func')#, args = json.dumps([[2,3]]))
    return HttpResponse("Done")


def bday_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour =10, minute = 4)
    task = PeriodicTask.objects.create(crontab=schedule, name="schdule_0mal8as_"+"13", task='sent_mail_app.tasks.bday_fun')
    return HttpResponse("Done")


