import json
import requests
import etcd3
from hydra import initialize, compose

class ConfigMicroservice:
    """
    A microservice that allows other microservices to read the configuration settings.
    """

    def __init__(self, etcd_host: str, etcd_port: str):
        self.etcd = etcd3.client(host=etcd_host, port=etcd_port)

    def get_config(self) -> dict:
        """
        Reads the configuration settings from the config microservice.

        Returns:
            dict: the configuration settings
        """
        response = self.etcd.get("/services/config")
        service_info = json.loads(response[0].decode("utf-8"))
        response = requests.get(f"http://{service_info['host']}:{service_info['port']}/{service_info['endpoint']}")
        config = json.loads(response.content.decode("utf-8"))
        return config


class EtcdMicroservice:
    """
    A microservice that allows other microservices to register themselves with etcd.
    """

    def __init__(self, etcd_host: str, etcd_port: str):
        self.etcd = etcd3.client(host=etcd_host, port=etcd_port)

    def register_service(self, service_name: str, endpoint: str) -> None:
        """
        Registers the microservice with etcd.

        Args:
            service_name (str): the name of the microservice
            endpoint (str): the URL endpoint for the microservice
        """
        service_info = {
            "host": "localhost",
            "port": 8000,
            "name": service_name,
            "endpoint": endpoint,
            "metadata": {"protocol": "http"},
        }

        self.etcd.put(f"/services/{service_name}", json.dumps(service_info))


class LoggingMicroservice:
    """
    A microservice that provides centralized logging for other microservices.
    """

    def __init__(self, etcd_host: str, etcd_port: str, config_service: ConfigMicroservice):
        self.etcd_host = etcd_host
        self.etcd_port = etcd_port
        self.config_service = config_service

    def setup_logging(self, logger_name: str) -> None:
        """
        Configures the logger to send logs to the logging microservice.

        Args:
            logger_name (str): the name of the logger
        """
        config = self.config_service.get_config()

        logger = logging.getLogger(logger_name)
        logger.setLevel(config["logging"]["level"])

        etcd_client = etcd3.client(host=self.etcd_host, port=self.etcd_port)
        service_data = etcd_client.get("/services/logging")
        if service_data:
            service_info = json.loads(service_data[0].decode("utf-8"))
            url = f"http://{service_info['host']}:{service_info['port']}/{service_info['endpoint']}"

            handler = logging.handlers.HTTPHandler(url, method='POST')
            formatter = logging.Formatter(config["logging"]["format"])
            handler.setFormatter(formatter)

            logger.addHandler(handler)

        else:
            print("Error: Logging microservice not found.")

        logger.info("Logging started.")


class RemoteLogger:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.url = None

        etcd_client = etcd3.client(host=config["etcd"]["host"], port=config["etcd"]["port"])
        service_data = etcd_client.get("/services/logging")
        if service_data:
            service_info = json.loads(service_data[0].decode("utf-8"))
            if all(key in service_info for key in ["host", "port", "endpoint"]):
                self.url = f"http://{service_info['host']}:{service_info['port']}/{service_info['endpoint']}"

    def log(self, level, message, **kwargs):
        self.logger.log(level, message, **kwargs)
        if self.url:
            log_data = {
                "level": level,
                "message": message,
                "extra": kwargs
            }
            requests.post(self.url, json=log_data)
