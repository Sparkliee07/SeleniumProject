'''
@package framework.loggers.logger_file2

Default loging to file, without any formatting
'''

import os
import factory
from logger import Logger


class LoggerFile(Logger):

    destination = None

    def __init__(self, **kw):
        logfile = None
        destination_path = None
        if 'separator' in kw:
            self.separator = kw['separator']
        if 'filename' in kw:
            logfile = kw['filename']
        if 'destination' not in kw:
            raise Exception('{}: Destination folder MUST be specified'.format(self.__class__.__name__))
        else:
            destination_path = kw['destination']
        self.destination = open(os.path.sep.join([destination_path, logfile]), 'a')

    def __del__(self):
        if self.destination:
            self.destination.close()

    def report(self, message, level=None):
        self.destination.write(message + '\n')
        self.destination.flush()


factory.register('file', LoggerFile)
