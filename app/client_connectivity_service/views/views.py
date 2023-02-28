from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View

from .views import front_page, register, success, login, logout, dashboard, errors

class FrontPageView(TemplateView):
    """
    Class-based view to display the front page of the application.
    """
    template_name = "ClientConnectivityModule/front_page.html"

class RegisterView(View):
    """
    Class-based view to handle user registration.
    """
    def get(self, request):
        """
        Handle GET request to display the registration form.
        """
        form = UserCreationForm()
        return render(request, 'ClientConnectivityModule/register.html', {'form': form})

    def post(self, request):
        """
        Handle POST request to process the registration form.
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('success')
        return render(request, 'ClientConnectivityModule/register.html', {'form': form})

class SuccessView(TemplateView):
    """
    Class-based view to display the success page after successful registration.
    """
    template_name = "ClientConnectivityModule/success.html"

class LoginView(View):
    """
    Class-based view to handle user login.
    """
    def get(self, request):
        """
        Handle GET request to display the login form.
        """
        return render(request, 'ClientConnectivityModule/login.html')

    def post(self, request):
        """
        Handle POST request to process the login form.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('login')

class LogoutView(View):
    """
    Class-based view to handle user logout.
    """
    def get(self, request):
        """
        Handle GET request to logout the user.
        """
        logout(request)
        return redirect('front_page')

class DashboardView(TemplateView):
    """
    Class-based view to display the dashboard after successful login.
    """
    template_name = "ClientConnectivityModule/dashboard.html"

class ErrorView(TemplateView):
    """
    Class-based view to display error pages.
    """
    template_name = "ClientConnectivityModule/errors.html"

