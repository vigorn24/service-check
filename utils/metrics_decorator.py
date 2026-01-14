from metrics import SERVICE_CALLS
import functools
import inspect

def service_metric(service_name: str):
    def decorator(func):
        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                SERVICE_CALLS.labels(
                    service=service_name,
                    function=func.__name__
                ).inc()
                return await func(*args, **kwargs)
            return wrapper
        return func
    return decorator
