import logging
from django.shortcuts import render
from django.conf import settings


class FrontPageView:
    """
    Class-based view to display the front page of the application.
    """
    template_name = "templates/html/front_page.html"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=settings.LOG_LEVEL,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(f"{settings.BASE_DIR}/logs/mednotes.log"),
                logging.StreamHandler()
            ]
        )

    def get(self, request):
        """
        Handle GET request to display the front page.
        """
        self.logger.info("Rendering front page")
        return render(request, self.template_name)

