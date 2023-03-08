import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from hydra.utils import instantiate

logger = logging.getLogger(__name__)

config = instantiate("config")

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
                logger.info(f"{username} registered successfully")
                return redirect(config.urls.dashboard)
            else:
                messages.error(request, "Error logging in after registration")
                logger.error("Error logging in after registration")
    else:
        form = UserRegistrationForm()

    return render(request, f"{config.templates_path}/html/register.html", {"form": form})

