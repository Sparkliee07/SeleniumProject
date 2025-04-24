"""@package framework.api2.factory
@brief File Purpose: Entry point to get access to any API installed in framework
@author: muthu
@version: 0.1
    02/12/2025
@copyright Physio-Control
@pre Test Subsystem: Framework API Base class

this module should be used by all test scripts or supplementary written in python
"""

from tms.framework import imp
import os

import ctx

modules = {}


def __init__(transport=None):
    global modules
    path = os.path.dirname(os.path.realpath(__file__))
    submodules = [subdir for subdir in os.listdir(path) if os.path.isdir(os.path.join(path, subdir))]
    for entry in submodules:
        f, filename, description = imp.find_module('__init__',
                                                   [os.path.join(os.path.dirname(os.path.realpath(__file__)), entry)]
                                                   )
        modules[entry] = imp.load_module(entry,
                                         f,
                                         filename,
                                         description
                                         )
        print('From module "{}" loaded: {}'.format(entry, modules[entry].apis))

__init__()


def get_list():
    """ returns list of all loaded modules
    """
    return modules.keys()


def get_instance(name):
    inst = modules[name].apis[0](ctx) if name in modules else None
    if inst:
        ctx.add_api_info(name + ':' + inst.get_version(silent=True))
    return inst
