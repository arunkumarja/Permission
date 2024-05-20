# forms.py
from django.forms import ModelForm
from .models import FileUpload

class UploadFileForm(ModelForm):
    model=FileUpload
    fields=['upload','upload_on']
    
