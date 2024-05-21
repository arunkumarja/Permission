from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'is_staff','password', 'is_superuser', 'is_active', 'last_login', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        user = User.objects.create(**validated_data)
        return user

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_type
        fields = ['is_teach', 'is_student', 'user']
    
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=FileUpload
        fields=['upload']    

class BlobModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=BlobModel
        fields=['blob']

class CSVFileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CSVFile
        fields=['csv']        

    