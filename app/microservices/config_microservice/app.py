import json
import logging
from typing import Any, Dict

import etcd3
from hydra import initialize, compose
from django.http import JsonResponse

# Load configuration settings from file
with initialize(config_path="./config/mednotes.yml"):
    config = compose(config_name="logging")
logging_config = config["logging"]

class ConfigMicroservice:
    """
    A microservice that allows other microservices to read the mednotes.yml config file.

    Args:
        etcd_host: str, hostname of the etcd server
        etcd_port: str, port number of the etcd server
        config_path: str, path to the config file
    """
    def __init__(self, etcd_host: str, etcd_port: str, config_path: str):
        self.etcd = etcd3.client(host=etcd_host, port=etcd_port)
        self.config = self._read_config_file(config_path)

    def _read_config_file(self, config_path: str) -> Dict[str, Any]:
        """
        Reads the mednotes.yml config file.

        Args:
            config_path: str, path to the config file

        Returns:
            Dict[str, Any], the configuration settings as a dictionary
        """
        with initialize(config_path=config_path):
            config = compose(config_name="mednotes")

        return config

    def get_config(self, request) -> JsonResponse:
        """
        Returns the configuration settings as a JSON response.

        Args:
            request: HttpRequest, the HTTP request object

        Returns:
            JsonResponse, the configuration settings as a JSON response
        """
        config_dict = {k: v for k, v in self.config.items()}
        return JsonResponse(config_dict)

    def register_with_etcd(self, service_name: str, endpoint: str) -> None:
        """
        Registers the configuration microservice with the etcd microservice.

        Args:
            service_name: str, name of the configuration microservice
            endpoint: str, the URL endpoint for the configuration microservice
        """
        service_info = {
            "host": logging_config["host"],
            "port": logging_config["port"],
            "name": service_name,
            "endpoint": endpoint,
            "metadata": {"protocol": "http"},
        }

        self.etcd.put(f"/services/{service_name}", json.dumps(service_info))


