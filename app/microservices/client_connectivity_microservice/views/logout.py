import hydra
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


@hydra.main(config_path="config", config_name="config")
def logout_view(request, cfg):
    """
    View to handle user logout.
    """
    logout(request)
    return redirect(cfg.defaults.front_page)

