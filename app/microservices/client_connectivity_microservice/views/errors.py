import logging
from django.shortcuts import render
from hydra.utils import get_original_cwd, instantiate

logger = logging.getLogger(__name__)
log_file = f"{get_original_cwd()}/logs/mednotes.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG)

config = instantiate("config")

class ErrorHandlers:
    """
    Class-based view to handle errors.
    """
    def handler404(self, request, exception):
        """
        Handle 404 error.
        """
        logger.warning(f"404 error occurred: {exception}")
        return render(request, f"{config.templates_path}/html/404.html", status=404)

    def handler500(self, request):
        """
        Handle 500 error.
        """
        logger.error("500 error occurred")
        return render(request, f"{config.templates_path}/html/500.html", status=500)

error_handlers = ErrorHandlers()

