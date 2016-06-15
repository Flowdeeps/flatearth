#!/usr/bin/env python

import subprocess
from subprocess import Popen, PIPE

cmd = "git log --follow documents/index.md"

term = subprocess.Popen( cmd, shell=True, stdout=PIPE, universal_newlines=True )
output = term.communicate()[ 0 ].split( "\n" )

# with open(output, 'r' ) as f:
#     for line in f:
#         print( line )
