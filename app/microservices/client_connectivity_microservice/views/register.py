from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from forms.forms import UserRegistrationForm


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

    return render(request, "/templates/html/register.html", {"form": form})

