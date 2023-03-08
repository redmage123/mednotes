import logging
import os
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hydra import initialize, compose
from etcd_registry import EtcdRegistry
from logrotate import LogRotate


class LoggingService:
    """
    Microservice that receives log messages from other microservices and appends them to a log file.

    Args:
        etcd_host: str, hostname of etcd server
        etcd_port: str, port number of etcd server
        etcd_ttl: int, time-to-live for etcd key
        log_dir: str, path to directory containing log files
        log_rotate: bool, whether to rotate logs
        log_rotate_frequency: str, frequency at which to rotate logs (e.g. weekly)
        log_rotate_max_age: int, maximum age of log files (in weeks)
        log_rotate_size: str, maximum size of log files (e.g. 100M)
    """
    def __init__(
        self,
        etcd_host: str,
        etcd_port: str,
        etcd_ttl: int,
        log_dir: str = "/app/logs",
        log_rotate: bool = True,
        log_rotate_frequency: str = "weekly",
        log_rotate_max_age: int = 10,
        log_rotate_size: str = "100M"
    ):
        self.etcd_registry = EtcdRegistry(etcd_host, etcd_port, etcd_ttl)
        self.log_dir = log_dir
        self.log_rotate = log_rotate
        self.log_rotate_frequency = log_rotate_frequency
        self.log_rotate_max_age = log_rotate_max_age
        self.log_rotate_size = log_rotate_size

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure logging
        self.log_file = os.path.join(log_dir, "mednotes.log")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Configure log rotation
        if log_rotate:
            self.log_rotator = LogRotate(
                self.log_file,
                frequency=log_rotate_frequency,
                max_age=log_rotate_max_age,
                size=log_rotate_size
            )
            self.log_rotator.start()

    def log_message(self, message: str) -> None:
        """
        Logs a message to the log file.

        Args:
            message: str, log message
        """
        self.logger.debug(message)

    def process_logs(self) -> None:
        """
        Processes log messages from other microservices and logs them to the log file.
        """
        while True:
            try:
                # Get next log message from etcd
                log_message = self.etcd_registry.get_next_log_message()
                if not log_message:
                    time.sleep(1)
                    continue

                # Log message to file
                self.log_message(log_message)

            except KeyboardInterrupt:
                break

        if self.log_rotate:
            self.log_rotator.stop()


# Initialize LoggingService
with initialize(config_path="/home/bbrelin/src/repos/mednotes/config"):
    config = compose(config_name="mednotes")
logging_service = LoggingService(
    etcd_host=config.etcd.host,
    etcd_port=config.etcd.port,
    etcd_ttl=config.etcd.ttl,
    log_dir=config.logging.log_dir,
    log_rotate=config.logging.log_rotate,
    log_rotate_frequency=config.logging.log_rotate_frequency,
    log_rotate_max_age=config

@csrf_exempt
def log(request):
    """
    Endpoint for receiving log messages from other microservices.

    Args:
        request: HttpRequest object containing log message in POST data

    Returns:
        JsonResponse object with status OK or ERROR
    """
    if request.method == "POST":
        log_data = request.POST.get("log_data")
        if log_data is not None:
            logging_service.log_message(log_data)
            return JsonResponse({"status": "OK"})
    return JsonResponse({"status": "ERROR"})


if __name__ == "__main__":
    # Start processing logs
    logging_service.process_logs()

