import logging
from django.shortcuts import render
from hydra.utils import instantiate

logger = logging.getLogger(__name__)

class FrontPageView:
    """
    Class-based view to display the front page of the application.
    """
    def __init__(self):
        self.config = instantiate("config")
        self.logger = logging.getLogger(__name__)

    def get(self, request):
        """
        Handle GET request to display the front page.
        """
        self.logger.info("Rendering front page")
        return render(request, self.config.templates.front_page)

