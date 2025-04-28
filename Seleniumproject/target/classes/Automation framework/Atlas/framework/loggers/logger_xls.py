 '''
@package framework.loggers.logger_xls

Default loging to file
'''

import os
import statistics

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

    def report(self, message, level='step'):
        if level == "scenario":
            formatted_message = self.separator.join(["Scenario: " + str(statistics.scenario), message.strip()])
        elif level == "status":
            formatted_message = self.separator.join(["Scenario status: ", message.strip().upper(), "\n"])
        elif level == "tc_status":
            formatted_message = self.separator.join(["Testcase status: ", message.strip().upper()])
        elif level == "node":
            formatted_message = self.separator.join(["Board name:", message])
        elif level == "start_time":
            formatted_message = self.separator.join(["Start time: ",
                                                     str(message.strftime('%Y/%m/%d %H:%M:%S')) + ' UTC'])
        elif level == "finish_time":
            formatted_message = self.separator.join(["Finish time: ",
                                                     str(message.strftime('%Y/%m/%d %H:%M:%S')) + ' UTC',
                                                     "\n"])
        elif level == "statistics":
            formatted_message = self.separator.join(["Scenarios statistics:", "\n" + message])
        elif level == 'step':
            formatted_message = self.separator.join(["Step: " + str(statistics.step), message.strip()])
        elif level == 'brief':
            formatted_message = ': '.join(['Brief', message.strip()])
        else:
            formatted_message = ' : '.join([self.get_timestamp(), message.strip()])
        print (formatted_message)
        self.destination.write(formatted_message + '\n')
        self.destination.flush()


factory.register('xls', LoggerFile)
