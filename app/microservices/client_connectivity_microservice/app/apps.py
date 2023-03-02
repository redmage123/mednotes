import logging
import os
import hydra
from hydra.core.config_store import ConfigStore
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View


cs = ConfigStore.instance()

@hydra.main(config_path='../../config', config_name='mednotes')
def run_app(cfg):
    cs.store(name='config', node=cfg)

    project_root = cfg.defaults.project_root

    log_file = os.path.join(project_root, 'logs/mednotes.log')
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(module)s %(message)s')

    class FrontPageView(TemplateView):
        """
        Class-based view to display the front page of the application.
        """
        template_name = "templates/html/front_page.html"

    class RegisterView(View):
        """
        Class-based view to handle user registration.
        """
        def get(self, request):
            """
            Handle GET request to display the registration form.
            """
            form = UserCreationForm()
            logging.debug('User accessed registration form')
            return render(request, 'templates/html/register.html', {'form': form})

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
                logging.info('User registered and logged in')
                return redirect('success')
            else:
                logging.error('Error with registration form')
            return render(request, 'templates/html/register.html', {'form': form})

    class SuccessView(TemplateView):
        """
        Class-based view to display the success page after successful registration.
        """
        template_name = "templates/html/success.html"

    class LoginView(View):
        """
        Class-based view to handle user login.
        """
        def get(self, request):
            """
            Handle GET request to display the login form.
            """
            return render(request, 'templates/html/login.html')

        def post(self, request):
            """
            Handle POST request to process the login form.
            """
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                logging.info('User logged in')
                return redirect('dashboard')
            else:
                logging.error('Error with login form')
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
            logging.info('User logged out')
            return redirect('front_page')

    class DashboardView(TemplateView):
        """
        Class-based view to display the dashboard after successful login.
        """
        template_name = "templates/html/dashboard.html"

    class ErrorView(TemplateView):
        """
        Class-based view to display error pages.
        """
        template_name = "templates/html/errors.html"


if __name__ == "__main__":
    run_app()

