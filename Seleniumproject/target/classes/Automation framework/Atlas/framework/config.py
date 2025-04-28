"""@package config
@brief File Purpose: Module is intended to load configuration for Test Framework
$Author: Muthu $
@version $Revision: #1 $
$Date: 2025/02/12 $
@copyright Teradyne Inc
@pre Infrastructure: none

@attention Dependencies: os, json

Description: Module is intended to load configuration for Test Framework
"""

import os
import json
import socket


CONFIGURATION_PATH = os.path.sep.join(['..', 'test_pc_configuration.json'])

infrastructure = None
settings = None


def load_configuration(file_name=CONFIGURATION_PATH, conf_type='test_pc'):
    """
    Function loads configuration file, parse it according to specified
        configuration type, so modules, which have needs in configuration,
        can obtain it from the common place.

    @param [in] file_name: string which represents path to configuration file.

    @return None
    """
    global infrastructure
    global settings
    f = open(file_name, 'r')
    config = json.load(f)
    # type of configuration can be stored in configuration file
    if conf_type == 'test_pc':
        # jenkins:
        infrastructure = config['infrastructure']
        settings = config['settings']
        settings['nodes']['path'] = os.path.sep.join(
            # this is not god idea fix path on a fly
            #  what id user specifies absolute path?!
            ['..',
             settings['nodes']['path']]
        )
        if 'jenkins' in infrastructure:
            if 'gui' in infrastructure['jenkins']['projects']:
                if 'qnx' in infrastructure['jenkins']['projects']['gui']:
                    qnx = infrastructure['jenkins']['projects']['gui']['qnx']
                    qnx_settings = settings['qnx']['applications']['gui']
                    qnx['binary'] = qnx_settings['name']
                    qnx['local_dir'] = qnx_settings['local_path']
        if 'perforce' in infrastructure:
            infrastructure['perforce']['Client'] = str(socket.gethostname())


load_configuration()
