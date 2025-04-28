'''

'''

import os
import json

import statistics

# logging support
import factory
from logger import Logger


class LoggerJson(Logger):

    destination = None
    document = {
        'status': 'pass',
        'statistics': {},
        'scenarios': [],
        }

    def __init__(self, **kw):
        filename = 'report.json'
        if 'separator' in kw:
            self.separator = kw['separator']
        if 'filename' in kw:
            filename = kw['filename']
        if 'destination' not in kw:
            raise Exception('{}: Destination folder MUST be specified'.format(self.__class__.__name__))
        self.destination = open(os.path.join(kw['destination'], filename), 'w')

    def __del__(self):
        if self.destination:
            self.destination.write(json.dumps(self.document))
            self.destination.close()

    def report(self, message, level):
        print(self.format.format(message=message, level=level))
        last_tc = len(self.document['scenarios']) - 1
        if level == "scenario":
            self.document['scenarios'].append(
                {
                    'number': statistics.scenario,
                    'name': message.strip(),
                    'status': 'pass',
                    'steps': [],
                }
            )
        elif level == "tc_status":
            self.document['status'] = message.strip().upper()
        elif level == "statistics":
            pass
        elif level == "node":
            self.document['node'] = message.strip()
        elif level == "status":
            self.document['scenarios'][last_tc]['status'] = message.strip().upper()
        elif level == "start_time":
            self.document['start_time'] = message.strftime('%Y/%m/%d %H:%M:%S')
        elif level == "finish_time":
            self.document['finish_time'] = message.strftime('%Y/%m/%d %H:%M:%S')
        elif level == 'step':
            data = message.strip().split(self.separator)
            self.document['scenarios'][last_tc]['steps'].append(
                {
                    'number': statistics.step,
                    'type': data[0],
                    'description': data[1],
                    'status': data[2],
                }
            )
        elif level == 'brief':
            self.document['Brief'] = message.strip()
        else:
            print('unsupported level "{}" in JSON format, skipped'.format(level))


factory.register('json', LoggerJson)
