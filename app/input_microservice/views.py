import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from .models import UploadedFile
from .serializers import UploadedFileSerializer


class FileUploadView(APIView):
    def post(self, request):
        file_obj = request.data['file']
        file_path = os.path.join(settings.MEDIA_ROOT, file_obj.name)

        with open(file_path, 'wb') as f:
            f.write(file_obj.read())

        file_data = {
            'path': file_path,
            'filename': file_obj.name,
            'content_type': file_obj.content_type,
            'size': os.path.getsize(file_path),
        }

        serializer = UploadedFileSerializer(data=file_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

