import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from hydra.utils import instantiate

logger = logging.getLogger(__name__)

cs = None


class FrontPageView(TemplateView):
    """
    Class-based view to display the front page of the application.
    """
    template_name = cs.views.front_page_template


class RegisterView(View):
    """
    Class-based view to handle user registration.
    """
    def get(self, request):
        """
        Handle GET request to display the registration form.
        """
        form = UserCreationForm()
        logger.debug('User accessed registration form')
        return render(request, cs.views.register_template, {'form': form})

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
            logger.info('User registered and logged in')
            return redirect(cs.views.success_url)
        else:
            logger.error('Error with registration form')
        return render(request, cs.views.register_template, {'form': form})


class SuccessView(TemplateView):
    """
    Class-based view to display the success page after successful registration.
    """
    template_name = cs.views.success_template


class LoginView(View):
    """
    Class-based view to handle user login.
    """
    def get(self, request):
        """
        Handle GET request to display the login form.
        """
        return render(request, cs.views.login_template)

    def post(self, request):
        """
        Handle POST request to process the login form.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info('User logged in')
            return redirect(cs.views.dashboard_url)
        else:
            logger.error('Error with login form')
            return redirect(cs.views.login_url)


class LogoutView(View):
    """
    Class-based view to handle user logout.
    """
    def get(self, request):
        """
        Handle GET request to logout the user.
        """
        logout(request)
        logger.info('User logged out')
        return redirect(cs.views.front_page_url)


class DashboardView(TemplateView):
    """
    Class-based view to display the dashboard after successful login.
    """
    template_name = cs.views.dashboard_template


class ErrorView(TemplateView):
    """
    Class-based view to display error pages.
    """
    template_name = cs.views.error_template


# instantiate views using Hydra
views_config = instantiate("views")
front_page_view = FrontPageView.as_view()
register_view = RegisterView.as_view()
success_view = SuccessView.as_view()
login_view = LoginView.as_view()
logout_view = LogoutView.as_view()
dashboard_view = DashboardView.as_view()
error_view = ErrorView.as_view()

