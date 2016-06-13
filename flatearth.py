#!/usr/bin/env python

import os
import configparser

import markdown
from bs4 import BeautifulSoup

import shutil

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
css_folder = assets + config['CSS']['cssfolder']
js_folder = assets + config['JS']['jsfolder']
img_folder = assets + config['IMG']['imgfolder']
# asset files
# tpl files
tpl_head_file = tpl_folder + config['TPL']['header']
tpl_aside_file = tpl_folder + config['TPL']['aside']
tpl_foot_file = tpl_folder + config['TPL']['footer']
# css file
css_file = css_folder + config['CSS']['cssfile']
# js file
js_file = js_folder + config['JS']['jsfile']

md_items = os.listdir( input_folder )
for md_item in md_items:
    if md_item.lower().endswith( '.md' ):
        input_md = md_item

md = markdown.Markdown( output_format = "html5" )

input_md = input_folder + input_md
input_md = open( input_md, 'r' ).read()
input_md = md.convert( input_md )
soup = BeautifulSoup( input_md, "html.parser" )
for html_elem in soup.find_all( 'h1' ):
    title_entity = html_elem.text
for img_elem in soup.find_all( 'img' ):
    picture_entity = img_elem
    # print(picture_entity)

body = input_md + '\n' # I like to have a new line at the end of all my html documents

head = open( tpl_head_file, 'r' ).read()
head = head.replace("$title", title_entity)
head = head.replace("$css", css_file)
head = head.replace("$js", js_file)

aside = open( tpl_aside_file, 'r' ).read()
foot = open( tpl_foot_file, 'r' ).read()

# check for css
new_css_folder = output_folder + css_folder
css_items = os.listdir( input_folder + css_folder )

i = 0
for css_item in css_items:
    if css_item.lower().endswith( '.css' ):
        i = i + 1
        if i > 0:
            if not os.path.exists( new_css_folder ):
                os.makedirs( new_css_folder )
            shutil.copy2( input_folder + css_folder + css_item, new_css_folder )

# check for images
new_img_folder = output_folder + img_folder
img_items = os.listdir( input_folder + img_folder )

i = 0
for img_item in img_items:
    file_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']
    for file_ext in file_exts:
        # print( file_ext )
        if img_item.lower().endswith( file_ext ):
            i = i + 1
            if i > 0:
                if not os.path.exists( new_img_folder ):
                    os.makedirs( new_img_folder )
                shutil.copy2( input_folder + img_folder + img_item, new_img_folder )

output_file = open( output_filename, 'w' )
output_file.write( head )
output_file.write( '\n' )
output_file.write( output_string )
output_file.write( '\n' )
output_file.write( "<body>" )
output_file.write( body )
output_file.write( '\n' )
output_file.write( aside )
output_file.write( "</body>" )
output_file.write( '\n' )
output_file.write( foot )
output_file.close()
