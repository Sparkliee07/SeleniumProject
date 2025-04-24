def expect_label(label):
    def decorator(func):
        func.expect_label = label
        return func
    return decorator
