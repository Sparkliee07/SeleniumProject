
import os
import statistics
import json
import ctx

from loggers import factory
from loggers.logger import Logger

debug_logger = None
report_loggers = []

separator = Logger.separator


def get_timestamp():
    return Logger().get_timestamp()


def save_srs_data():
    srs = json.dumps(statistics.SRS)
    logfile = open(os.path.join(ctx.LOG_DIR, 'srs_data.txt'), 'w')
    logfile.write(srs)
    logfile.close()


def report(message, level='step'):
    for lg in report_loggers:
        lg.report(message, level)


def debug(message):
    debug_logger.report(message, level=None)


def custom_loger(name, log_type='file', destination=None):
    if not destination:
        destination = ctx.LOG_DIR
    return factory.get_logger(log_type)(filename=name, destination=destination)


def initialize(loggers=['xls', 'json'], destination=None):

    if not destination:
        destination = ctx.LOG_DIR

    print('Setup loggers: {}'.format(loggers))

    if 'xls' in loggers:
        report_loggers.append(factory.get_logger('xls')(filename="report.xls",
                                                        destination=destination))
    if 'json' in loggers:
        report_loggers.append(factory.get_logger('json')(filename="report.json",
                                                         destination=destination))
    if 'junit' in loggers:
        report_loggers.append(factory.get_logger('junit')(filename="report.xml",
                                                          destination=destination))


def done():
    global report_loggers
    while len(report_loggers):
        gl = report_loggers.pop()
        del gl

# debug log should be available from start - so it's static
DEBUG_LOG_DIR = "debug_logs"
ctx.START_TIME = get_timestamp()

DEBUG_LOG_FILENAME = os.path.abspath(os.path.join(DEBUG_LOG_DIR, "log_" + ctx.START_TIME + ".txt"))
if not os.path.exists(DEBUG_LOG_DIR):
    os.makedirs(DEBUG_LOG_DIR)

debug_logger = factory.get_logger('xls')(filename="log_" + ctx.START_TIME + ".txt",
                                         destination=os.path.abspath(DEBUG_LOG_DIR))
