from rest_framework.views import APIView
from rest_framework.response import Response 
from .models import *
# from serializers import *
from django.http import JsonResponse
from .serializers import UserSerializer,FileSerializer,BlobModelSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.parsers import FileUploadParser
import pandas as pd


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({"message":serializer.data})  
        

class FileUpload(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=201)
        else:
            return Response(file_serializer.errors, status=400)   


class BlobModelAPI(APIView):
    parser_class = (MultiPartParser, FormParser)
    def post(self,request):
        file=request.FILES.get('file')
        if file:
            file_content = file.read() 
        #     print(file_content)
        #     serializer=BlobModelSerializer(data={'fun':file_content})
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response("successfully uplaoded file ")
        #     return Response(serializer.errors)
        # return Response("No file provided.", status=400)        

            blob=BlobModel.objects.create(name='fun',blob=file_content)
            blob.save()
        return Response("success")

class CSVFileAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self,request,*args,**kwargs):
        try:

            file = request.FILES.get('file')
            if not file:
                return Response({"error": "No file provided"})
            try:
                df= pd.read_csv(file)
                json_data=f=df.to_dict()
            except Exception as e:
                return Response({"error":str(e)})
            data=CSVFile(csv=json_data)   
            data.save()
            return Response({"message": "File successfully uploaded and data saved"})
        except Exception as e:
            return Response({"error":str(e)})      
