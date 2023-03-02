import os

import hydra
from django.core.wsgi import get_wsgi_application
from omegaconf import DictConfig


@hydra.main(config_path="../../../config", config_name="mednotes")
def main(cfg: DictConfig) -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", cfg.settings_module)

    application = get_wsgi_application()

    # Use the primary function as an entry point to hydra
    # to load the configuration and apply it to Django settings
    main()

