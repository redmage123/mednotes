import logging
import os

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from hydra.utils import get_original_cwd

logger = logging.getLogger(__name__)

class SuccessView:
    def __init__(self, cfg):
        self.cfg = cfg

        log_file = os.path.join(self.cfg.defaults.log_dir, 'mednotes.log')
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(module)s %(message)s'
        )

    @api_view(['GET'])
    def get_audio_file(self, request):
        try:
            audio_file = open(os.path.join(self.cfg.defaults.data_dir, 'audio', 'audio.mp3'), 'rb')
            response = HttpResponse(audio_file.read(), content_type='audio/mp3')
            response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
            return response
        except Exception as e:
            logger.error(f"Failed to get audio file: {str(e)}")
            return render(request, 'error.html', status=500)

