import logging
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from utils.logging_config import request_id_var, user_id_var

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for structured request/response logging"""

    async def dispatch(self, request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        request_id_var.set(request_id)

        # Extract user ID from auth token if present
        auth_header = request.headers.get('authorization', '')
        if auth_header.startswith('Bearer '):
            try:
                # Decode token to get user ID (simplified)
                token = auth_header.split(' ')[1]
                # You'd decode the JWT here - placeholder
                user_id_var.set('user_from_token')
            except Exception:
                pass

        # Log request start
        start_time = time.time()
        logger.info("Request started", extra={
            'method': request.method,
            'path': request.url.path,
            'query_params': str(request.query_params),
            'client_ip': request.client.host
        })

        # Process request
        try:
            response = await call_next(request)

            # Log request completion
            duration_ms = (time.time() - start_time) * 1000
            logger.info("Request completed", extra={
                'method': request.method,
                'path': request.url.path,
                'status_code': response.status_code,
                'duration_ms': round(duration_ms, 2)
            })

            return response
        except Exception as e:
            # Log errors
            logger.error("Request failed", extra={
                'method': request.method,
                'path': request.url.path,
                'error': str(e),
                'error_type': type(e).__name__
            }, exc_info=True)
            raise
