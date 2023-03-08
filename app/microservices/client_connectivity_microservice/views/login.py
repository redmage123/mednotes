from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View
from hydra.utils import instantiate
import logging

logger = logging.getLogger(__name__)

class LoginView(View):
    """
    Class-based view to handle user login.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = instantiate("config")
        self.logging_config = instantiate("logging")

    def get(self, request):
        """
        Handle GET request to display the login form.
        """
        return render(request, f"{self.config.templates_path}/html/login.html")

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

