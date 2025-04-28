'''
@package framework.loggers.logger

this module define appi for logger and implement basic terminal loger
'''

import factory
import datetime


class Logger:

    separator = '\t'
    format = '[{level}] {message}'

    def get_timestamp(self):
        raw_datetime = datetime.datetime.utcnow()
        date_split = str(raw_datetime).split(' ')
        timestamp = date_split[0] + "_" + date_split[1].split('.')[0].replace(':', '-')
        return timestamp

    def __init__(self, **kw):
        pass

    def report(self, message, level):
        print(self.format.format(message=message, level=level))


factory.register('default', Logger)
