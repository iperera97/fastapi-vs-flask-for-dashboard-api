import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def time_log(service_name="unknown"):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            logger.info(
                f"{service_name} executed in {duration:.4f} seconds for {func.__name__}"
            )
            return result

        return wrapper
    return decorator


class QueryEngineException(Exception):
    ...