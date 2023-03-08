
import logging
from django.shortcuts import render
from hydra.utils import get_original_cwd, instantiate

logger = logging.getLogger(__name__)
logging.basicConfig(filename=f"{get_original_cwd()}/logs/mednotes.log", level=logging.DEBUG)

config = instantiate("config")


def success(request):
    return render(request, f"{config.templates_path}/html/success.html")

