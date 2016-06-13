#!/usr/bin/env python

import os
import markdown

import configparser

config = configparser.ConfigParser()
config.sections()
config.read( 'general.ini' )
config.sections()

input_folder = config['APP']['inputfolder']
output_folder = config['APP']['outputfolder']
output_filename = output_folder + config['APP']['outputfile']
output_string = config['APP']['outputstring']
output_string = "<!-- " + output_string + " -->"
assets = config['SITE']['assets']
# asset folders
tpl_folder = input_folder + assets + config['TPL']['tplfolder']
css_folder = input_folder + assets + config['CSS']['cssfolder']
js_folder = input_folder + assets + config['JS']['jsfolder']
# asset files
# tpl files
tpl_head_file = tpl_folder + config['TPL']['header']
tpl_aside_file = tpl_folder + config['TPL']['aside']
tpl_foot_file = tpl_folder + config['TPL']['footer']
# css file
css_file = assets + css_folder + config['CSS']['cssfile']
# js file
js_file = assets + js_folder + config['JS']['jsfile']

md = markdown.Markdown( output_format = "html5" )

items = os.listdir( input_folder )
for item in items:
    if item.lower().endswith( '.md' ):
        input_md = item

input_md = input_folder + input_md
input_md = open( input_md, 'r' ).read()
input_md = md.convert( input_md )

body = input_md + '\n' # I like to have a new line at the end of all my html documents

head = open( tpl_head_file, 'r' ).read()
aside = open( tpl_aside_file, 'r' ).read()
foot = open( tpl_foot_file, 'r' ).read()

output_file = open( output_filename, 'w' )
output_file.write( head )
output_file.write( '\n' )
output_file.write( output_string )
output_file.write( '\n' )
output_file.write( body )
output_file.write( '\n' )
output_file.write( aside )
output_file.write( '\n' )
output_file.write( foot )
output_file.close()
