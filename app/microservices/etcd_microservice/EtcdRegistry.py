import signal
import os
import logging
from typing import Optional
from etcd3 import Client
import hydra


logger = logging.getLogger(__name__)


class EtcdRegistry:
    def __init__(self, host: str, port: str, ttl: int):
        self.client = Client(host=host, port=port)
        self.ttl = ttl

    def register_service(self, name: str, url: str):
        key = f"/services/{name}/{url}"
        self.client.put(key, url, lease=self.client.lease(self.ttl))

    def unregister_service(self, name: str, url: str):
        key = f"/services/{name}/{url}"
        self.client.delete(key)


@hydra.main(config_path="", config_name="mednotes")
def run_etcd_service(cfg):
    project_root = os.environ.get("PROJECT_ROOT", cfg.defaults.project_root)
    config_path = getattr(cfg, "config_path", None)
    if config_path is None:
        config_path = os.path.join(project_root, "config")
    else:
        config_path = os.path.join(project_root, config_path)

    registry = EtcdRegistry(cfg.etcd_microservice.etcd_url.host,
                            cfg.etcd_microservice.etcd_url.port,
                            cfg.etcd_microservice.etcd_ttl)

    def sigterm_handler(_signo, _stack_frame):
        logger.info("Received SIGTERM, unregistering service...")
        registry.unregister_service("etcd", f"{os.environ['HOSTNAME']}:{os.environ['PORT']}")
        logger.info("Service unregistered, exiting.")
        exit(0)

    signal.signal(signal.SIGTERM, sigterm_handler)

    logger.info("Registering service...")
    registry.register_service("etcd", f"{os.environ['HOSTNAME']}:{os.environ['PORT']}")
    logger.info("Service registered.")

    signal.pause()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_etcd_service()

