from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .forms.forms import UserLoginForm, UserRegistrationForm, UploadFileForm
from .forms.forms import ProfileCreationForm, ProfileUpdateForm

import requests
import os

BASE_URL = "http://localhost:8000/api/"

@login_required
def dashboard(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES["file"]
            upload_file_url = BASE_URL + "upload_file/"
            response = requests.post(upload_file_url, files={"file": audio_file})
            if response.status_code == status.HTTP_201_CREATED:
                return redirect("success")
            else:
                messages.error(request, "Error occurred during file upload")
    else:
        form = UploadFileForm()

    return render(request, "dashboard.html", {"form": form})

def index(request):
    return render(request, "index.html")

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("index")

def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Error logging in after registration")
    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})

def success(request):
    return render(request, "success.html")

def index(request):
    return render(request, "index.html")

def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("index")

def user_registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Error logging in after registration")
    else:
        form = UserRegistrationForm()

    return render(request, "register.html", {"form": form})
