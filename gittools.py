#!/usr/bin/env python

import subprocess
from subprocess import Popen, PIPE

git_origin = []

def gitorigin ():
    cmd = "git remote -v"

    term = subprocess.Popen( cmd, shell=True, stdout=PIPE, universal_newlines=True )
    current_remote = term.communicate()[ 0 ]
    current_remote = current_remote.split( "\n" )

    for remote in current_remote:
        git_origin.append( remote )

    return git_origin

git_data = None

def githead ():
    cmd = "git rev-parse HEAD"

    term = subprocess.Popen( cmd, shell=True, stdout=PIPE, universal_newlines=True )
    current_revision = term.communicate()[ 0 ]
    current_revision = current_revision.replace( "\n", "" )

    git_data = current_revision

    return git_data

history_list = []

def load_data ( name, line, num ):
    if line.startswith( name ):
        tmp_name = line
        tmp_name = tmp_name.lstrip()
        history_list[ num - 1 ].append( tmp_name )

def githistory( file ):

    cmd = "git log --follow " + file

    term = subprocess.Popen( cmd, shell=True, stdout=PIPE, universal_newlines=True )
    output = term.communicate()[ 0 ].split( "\n" )

    i = 0
    j = 0
    for line in output:
        if line != "":
            if (i % 4 == 0):
                history_list.append( [] )
                j = j + 1
            load_data( "commit", line, j )
            load_data( "Author: ", line, j )
            load_data( "Date:", line, j )
            load_data( "   ", line, j )
            i = i + 1

    return history_list
