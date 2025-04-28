from functools import wraps

def test_param(optional=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.is_test_param = True
        wrapper.optional = optional
        return wrapper
    return decorator
