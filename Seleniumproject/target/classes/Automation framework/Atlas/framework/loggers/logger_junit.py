'''
@package framework.loggers.logger_junit

Logger engint to store logs in JUnit format
'''

import os
import junit_xml
from datetime import datetime

import factory
from logger import Logger


class LoggerJUnit(Logger):

    start_time = None
    end_time = None

    destination = None

    steps = []
    junit_testcases = []

    def __init__(self, **kw):
        if 'filename' in kw:
            logfile = kw['filename']
        if 'destination' not in kw:
            raise Exception('{}: Destination folder MUST be specified'.format(self.__class__.__name__))
        else:
            destination_path = kw['destination']
        self.destination = open(os.path.sep.join([destination_path, logfile]), 'w')

#         junit_testcase = junit_xml.TestCase(name, classname, elapsed_sec, stdout, stderr)

    def __del__(self):
        if self.destination:
            junit_suite = junit_xml.TestSuite("Junit Report",
                                              test_cases=self.junit_testcases,
                                              hostname=self.node,
                                              id=None,
                                              package=None,
                                              timestamp=self.start_time,
                                              properties={'status': self.tc})
            junit_suite.to_file(self.destination, [junit_suite])

    def report(self, message, level='step'):
        print(self.format.format(message=message, level=level))
        if level == "scenario":
            self.scenario_name = message
            self.scenario_start = datetime.now()
            pass
        elif level == "tc_status":
            # aka test suit in JUnit
            print('tc_status: {}'.format(message))
            self.tc = message
            pass
        elif level == "statistics":
            pass
        elif level == "node":
            self.node = message
        elif level == "status":
            # aka test case in JUnit
            # complete of sing test case
            self.junit_testcases.append(junit_xml.TestCase(self.scenario_name,
                                                           classname=None,
                                                           elapsed_sec=(datetime.now()-self.scenario_start).seconds,
                                                           stdout='\n'.join(self.steps),
                                                           stderr=None))
            if message == 'error':
                self.junit_testcases[-1].add_error_info(message)
            elif message == 'fail':
                self.junit_testcases[-1].add_failure_info(message)
            self.steps = []
        elif level == "start_time":
            self.start_time = str(message)
        elif level == "finish_time":
            self.end_time = str(message)
        elif level == 'step':
            self.steps.append(' : '.join([self.get_timestamp(), message.strip()]))
        else:
            pass


factory.register('junit', LoggerJUnit)

