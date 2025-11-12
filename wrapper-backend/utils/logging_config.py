import logging
import sys
from pythonjsonlogger import jsonlogger
from contextvars import ContextVar

# Context variables for request tracking
request_id_var: ContextVar[str] = ContextVar('request_id', default='')
user_id_var: ContextVar[str] = ContextVar('user_id', default='')

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter that includes context vars"""
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['request_id'] = request_id_var.get()
        log_record['user_id'] = user_id_var.get()
        log_record['service'] = 'wrapper-backend'

def setup_logging(level=logging.INFO):
    """Configure structured logging for the application"""
    handler = logging.StreamHandler(sys.stdout)
    formatter = CustomJsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s',
        rename_fields={'asctime': '@timestamp', 'levelname': 'severity'}
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(handler)

    # Reduce noise from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("watchdog").setLevel(logging.WARNING)
