from rest_framework.views import APIView
from rest_framework.response import Response 
from .models import *
# from serializers import *
from django.http import JsonResponse
from .serializers import UserSerializer


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer,"serializer")
        print(serializer.is_valid())
        try:
            if serializer.is_valid():
                serializer.save()
        except Exception as e:
            print(e)
        return JsonResponse({"message":serializer.data})  
        


