from pathlib import Path

import hydra
from omegaconf import DictConfig


@hydra.main(config_path="../../../config", config_name="mednotes")
def main(cfg: DictConfig) -> None:
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = cfg.secret_key

    DEBUG = cfg.debug

    ALLOWED_HOSTS = cfg.allowed_hosts

    INSTALLED_APPS = cfg.installed_apps

    MIDDLEWARE = cfg.middleware

    ROOT_URLCONF = cfg.root_urlconf

    TEMPLATES = cfg.templates

    WSGI_APPLICATION = cfg.wsgi_application

    DATABASES = cfg.databases

    AUTH_PASSWORD_VALIDATORS = cfg.auth_password_validators

    LANGUAGE_CODE = cfg.language_code

    TIME_ZONE = cfg.time_zone

    USE_I18N = cfg.use_i18n

    USE_TZ = cfg.use_tz

    STATIC_URL = cfg.static_url

    DEFAULT_AUTO_FIELD = cfg.default_auto_field

    # Use the primary function as an entry point to hydra
    # to load the configuration and apply it to Django settings
    main()

