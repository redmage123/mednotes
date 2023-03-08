import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import status
from forms.forms import UploadFileForm
from hydra.utils import get_original_cwd
from app.Microservices import ConfigMicroservice, LoggingMicroservice

config_service = ConfigMicroservice()
logging_service = LoggingMicroservice()

logger = logging_service.get_logger(__name__)
log_file = f"{get_original_cwd()}/logs/mednotes.log"

@login_required
def dashboard(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES["file"]
            upload_file_url = f"{config_service.get_config('upload_service_url')}/api/upload_file/"
            response = requests.post(upload_file_url, files={"file": audio_file})
            if response.status_code == status.HTTP_201_CREATED:
                return redirect("success")
            else:
                messages.error(request, "Error occurred during file upload")
                logger.error("Error occurred during file upload")
    else:
        form = UploadFileForm()

    return render(request, "templates/html/dashboard.html", {"form": form})

