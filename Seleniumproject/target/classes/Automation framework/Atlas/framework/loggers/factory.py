'''
Entry point to supported logging formats
'''

loggers = {}


def get_supported():
    return loggers.keys()


def get_logger(name):
    return loggers.get(name, None)


def register(name, logger):
    loggers[name] = logger
