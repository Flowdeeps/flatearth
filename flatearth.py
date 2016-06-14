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

input_folder = config[ 'APP' ][ 'inputfolder' ]
document_folder = config[ 'APP' ][ 'docfolder' ] # why is this specified independently? Because you might want a seperation of theme and content.
output_folder = config[ 'APP' ][ 'outputfolder' ]
output_filename = output_folder + config[ 'APP' ][ 'outputfile' ]
output_string = config[ 'APP' ][ 'outputstring' ]
output_string = "<!-- " + output_string + " -->"

# asset folders
assets = config[ 'SITE' ][ 'assets' ]
tpl_folder = input_folder + assets + config[ 'TPL' ][ 'tplfolder' ]
css_folder = assets + config[ 'CSS' ][ 'cssfolder' ]
js_folder = assets + config[ 'JS' ][ 'jsfolder' ]
img_folder = config[ 'IMG' ][ 'imgfolder' ]
# asset files
# tpl files
tpl_head_file = tpl_folder + config[ 'TPL' ][ 'header' ]
tpl_aside_file = tpl_folder + config[ 'TPL' ][ 'aside' ]
tpl_foot_file = tpl_folder + config[ 'TPL' ][ 'footer' ]
# css file
css_file = css_folder + config[ 'CSS' ]['cssfile']
# js file
js_file = js_folder + config[ 'JS' ][ 'jsfile' ]
# img sizes
img_max = config[ 'IMG' ][ 'imgmax' ]
img_mid = config[ 'IMG' ][ 'imgmid' ]
img_min = config[ 'IMG' ][ 'imgmin' ]
# picture breakpoints
# there's only two as the lareg image is the default img src
break_mid = config['IMG']['breakmid']
break_min = config['IMG']['breakmin']

md_items = os.listdir( document_folder )
for md_item in md_items:
    if md_item.lower().endswith( '.md' ):
        input_md = md_item

md = markdown.Markdown( output_format = "html5" )

import re

input_md = document_folder + input_md
input_md = open( input_md, 'r' ).read()
input_md = md.convert( input_md )
soup = BeautifulSoup( input_md, 'html5lib' )
for html_elem in soup.find_all( 'h1' ):
    title_entity = html_elem.text
for img_elem in soup.find_all( 'img' ):
    picture_entity = img_elem
    picture_parent = picture_entity.parent
    picture_src = picture_entity[ 'src' ] # ensure that all images are local, we don't want to get into hotlinking
    picture_alt = picture_entity[ 'alt' ]
    # this is where we'll run the image conversion function against the url we have
    new_picture_entity_parent = soup.new_tag( 'picture' )
    picture_parent.replaceWith( new_picture_entity_parent )
    new_picture_src = soup.new_tag( 'img' )
    new_picture_src[ 'src' ] = picture_src
    new_picture_src[ 'alt' ] = picture_alt
    new_picture_entity_parent.insert( 1, new_picture_src )
    i = 0
    while i < 2:
        if i == 1:
            new_picture_src1 = soup.new_tag( 'source' )
            new_picture_src1[ 'media' ] = "( min-width: " + break_mid + "px )"
            new_picture_src1[ 'srcset' ] = picture_src
            new_picture_entity_parent.insert( 1, new_picture_src1 )
        else:
            new_picture_src2 = soup.new_tag( 'source' )
            new_picture_src2[ 'media' ] = "( min-width: " + break_min + "px )"
            new_picture_src2[ 'srcset' ] = picture_src
            new_picture_entity_parent.insert( 1, new_picture_src2 )
        i = i + 1
    soup = str( soup ).replace( "</source>", "" ) # it's dirty but we've already performed our transformations
print( soup )

body = soup + '\n' # I like to have a new line at the end of all my html documents

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
