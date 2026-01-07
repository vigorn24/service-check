import logging
import functools
import inspect

def log_call(logger_name: str | None = None):
    def decorator(func):
        logger = logging.getLogger(logger_name or func.__module__)

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                logger.info("→ %s args=%s kwargs=%s", func.__name__, args, kwargs)
                result = await func(*args, **kwargs)
                logger.info("← %s result=%s", func.__name__, result)
                return result
            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            logger.info("→ %s args=%s kwargs=%s", func.__name__, args, kwargs)
            result = func(*args, **kwargs)
            logger.info("← %s result=%s", func.__name__, result)
            return result

        return sync_wrapper
    return decorator
