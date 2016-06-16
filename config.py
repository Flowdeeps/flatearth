#!/usr/bin/env python

import configparser

def getconfig ( input ):

    config = configparser.ConfigParser()
    config.sections()
    config.read( input )
    config.sections()
    config_dict={}

    for section in config:
        for var in config[ section ]:
            config_dict[ var ] = config[ section ][ var ]

    if ( config_dict[ "output_string" ] != None ):
        config_dict[ "output_string" ] = "<!-- " + config_dict[ "output_string" ] + " -->"

    return config_dict
