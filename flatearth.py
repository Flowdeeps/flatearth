#!/usr/bin/env python

import os
import markdown

input_dir = 'content'
output_dir = 'output'

md = markdown.Markdown( output_format = "html5" )

items = os.listdir( input_dir )
for item in items:
    if item.lower().endswith( '.md' ):
        input_md = item

input_md = input_dir + "/" + input_md
input_md = open( input_md, 'r' ).read()
input_md = md.convert( input_md )

body = input_md

head = open( 'content/assets/tpl/header.html', 'r' ).read()
aside = open( 'content/assets/tpl/aside.html', 'r' ).read()
foot = open( 'content/assets/tpl/footer.html', 'r' ).read()

output_file = open( output_dir + '/index.html', 'w' )
output_file.write( head )
output_file.write( body )
output_file.write( aside )
output_file.write( foot )
output_file.close()
