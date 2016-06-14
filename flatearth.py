#!/usr/bin/env python

from __future__ import print_function

import os
import configparser

import markdown
from bs4 import BeautifulSoup

from PIL import Image

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
# img sizes
img_max = config['IMG']['imgmax']
img_mid = config['IMG']['imgmid']
img_min = config['IMG']['imgmin']

md_items = os.listdir( input_folder )
for md_item in md_items:
    if md_item.lower().endswith( '.md' ):
        input_md = md_item

md = markdown.Markdown( output_format = "html5" )

input_md = input_folder + input_md
input_md = open( input_md, 'r' ).read()
input_md = md.convert( input_md )
soup = BeautifulSoup( input_md, 'html5lib' )
for html_elem in soup.find_all( 'h1' ):
    title_entity = html_elem.text
for img_elem in soup.find_all( 'img' ):
    picture_entity = img_elem

body = input_md + '\n' # I like to have a new line at the end of all my html documents

head = open( tpl_head_file, 'r' ).read()
head = head.replace( "$title", title_entity )
head = head.replace( "$css", css_file )
head = head.replace( "$js", js_file )

aside = open( tpl_aside_file, 'r' ).read()
foot = open( tpl_foot_file, 'r' ).read()

# check for css
new_css_folder = output_folder + css_folder
css_items = os.listdir( input_folder + css_folder )

i = 0
for css_item in css_items:
    if css_item.lower().endswith( ".css" ):
        i = i + 1
        if i > 0:
            if not os.path.exists( new_css_folder ):
                os.makedirs( new_css_folder )
            shutil.copy2( input_folder + css_folder + css_item, new_css_folder )

# check for images
new_img_folder = output_folder + img_folder
img_items = os.listdir( input_folder + img_folder )

i = 0
file_exts = [ ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"]
for img_item in img_items:
    for file_ext in file_exts:
        # print( file_ext )
        if img_item.lower().endswith( file_ext ):
            i = i + 1
            if i > 0:
                if not os.path.exists( new_img_folder ):
                    os.makedirs( new_img_folder )
                if file_ext == ".gif": # this is where we're going to check if it's an animated gif or not
                    # Image is a gif so has to be checked
                    img = Image.open( input_folder + img_folder + img_item )
                    img_copy = img.copy()
                    if img.is_animated:
                        # Image is an animated gif, move it without editing
                        shutil.copy2( input_folder + img_folder + img_item, new_img_folder ) # just copy it without editing
                    else: # image is not animated and can be resized
                        # Image is not an animated gif, edit it and move on
                        n = 0
                        while n < 3:
                            if n == 0:
                                if not img_copy.size[ 0 ] < int( img_max ):
                                    img_copy.size = int( img_max ), int( img_max )
                                    tmp_name = new_img_folder + "max_" + img_item
                                    img_copy.save( tmp_name )
                                else:
                                    shutil.copy2( input_folder + img_folder + img_item, new_img_folder )
                            if n == 1:
                                if not img_copy.size[ 0 ] < int( img_mid ):
                                    img_copy.size = int( img_mid ), int( img_mid )
                                    tmp_name = new_img_folder + "mid_" + img_item
                                    img_copy.save( tmp_name )
                                else:
                                    shutil.copy2( input_folder + img_folder + img_item, new_img_folder )
                            if n == 2:
                                if not img_copy.size[ 0 ] < int( img_min ):
                                    img_copy.size = int(img_min), int(img_min)
                                    tmp_name = new_img_folder + "min_" + img_item
                                    img_copy.save( tmp_name )
                                else:
                                    shutil.copy2( input_folder + img_folder + img_item, new_img_folder )
                            n = n + 1
                else:
                    # Image is not a gif so can be dicked with
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
