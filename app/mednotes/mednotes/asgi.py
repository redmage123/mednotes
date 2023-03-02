iimport os

import hydra
from django.core.asgi import get_asgi_application
from omegaconf import DictConfig


@hydra.main(config_path="../../../config/config", config_name="mednotes")
def main(cfg: DictConfig) -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", cfg.settings_module)

    application = get_asgi_application()

    # Use the primary function as an entry point to hydra
    # to load the configuration and apply it to Django settings
    main()

