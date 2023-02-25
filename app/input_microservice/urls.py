from django.urls import path
from .views import FileUploadView

app_name = 'input_microservice'

urlpatterns = [
    path('', FileUploadView.as_view(), name='file_upload'),
]

