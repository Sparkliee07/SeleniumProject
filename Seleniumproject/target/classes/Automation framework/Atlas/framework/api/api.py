"""@package framework.api.api
@brief File Purpose: Module defined class which should be used as base for all Framework API's
@author: Andriy Ohorodnyk (andriy.ohorodnyk@globallogic.com)
@version: 0.1
    6/10/2014
@copyright Physio-Control
@pre Test Subsystem: Framework API Base class

This class should be used as base calss by all  developers who adds new API's for Framewok
this class will be used by Factory to identify installed API's and export for Test cases
"""


class Api:
    def get_name(self):
        pass

    def get_version(self, silent=False):
        return 'ApiStub-IMPLEMENT!'

    def get_help(self):
        return "API provider should use this function for return human readable usage instruction"
