from rest_framework.views import APIView
from rest_framework.response import Response 
from .models import *
# from serializers import *
from django.http import JsonResponse
from .serializers import UserSerializer,FileSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.parsers import FileUploadParser



class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({"message":serializer.data})  
        


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .form import UploadFileForm


class FileUpload(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=201)
        else:
            return Response(file_serializer.errors, status=400)   

