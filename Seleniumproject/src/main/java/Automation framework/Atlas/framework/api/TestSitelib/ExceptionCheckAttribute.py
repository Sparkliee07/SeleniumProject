from functools import wraps

def ExceptionChecker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Example usage
@ExceptionChecker
def CheckException(expect, actual):
    # Example implementation of the exception checker method
    pass