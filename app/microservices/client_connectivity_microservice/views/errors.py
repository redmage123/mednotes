import requests
from django.shortcuts import render
from hydra.utils import instantiate


config_microservice_url = "http://config-microservice:8000"
logging_microservice_url = "http://logging-microservice:8000"

config = instantiate(requests.get(f"{config_microservice_url}/config").json())

class ErrorHandlers:
    """
    Class-based view to handle errors.
    """
    def handler404(self, request, exception):
        """
        Handle 404 error.
        """
        requests.post(f"{logging_microservice_url}/logs", data={"log_level": "warning", "log_message": f"404 error occurred: {exception}"})

        return render(request, f"{config.templates_path}/html/404.html", status=404)

    def handler500(self, request):
        """
        Handle 500 error.
        """
        requests.post(f"{logging_microservice_url}/logs", data={"log_level": "error", "log_message": "500 error occurred"})

        return render(request, f"{config.templates_path}/html/500.html", status=500)


error_handlers = ErrorHandlers()

