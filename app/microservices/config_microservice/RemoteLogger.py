import logging
import logging.handlers

class RemoteLogger:
    def __init__(self, logger_name, logging_config):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging_config["level"])
        handler = logging.handlers.SysLogHandler(address=(logging_config["host"], logging_config["port"]))
        formatter = logging.Formatter(logging_config["format"])
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, level, message, **kwargs):
        self.logger.log(level, message, **kwargs)
