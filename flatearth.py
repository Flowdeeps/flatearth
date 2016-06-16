#!/usr/bin/env python

from __future__ import print_function

import os, markdown, shutil

from bs4 import BeautifulSoup
from githistory import githistory
from PIL import Image
from config import config # this is from config.py - feed it the ini_file string and it will return my_config with named keys - eg: my_config[ "your_config_parameter" ]

ini_file = "general.ini"

my_config = config( ini_file )

md_items = os.listdir( my_config[ "document_folder" ] )
for md_item in md_items:
    if md_item.lower().endswith( '.md' ):
        input_md = md_item

md = markdown.Markdown( output_format = "html5" )

input_md = my_config[ "document_folder" ] + input_md
input_md = open( input_md, 'r' ).read()
input_md = md.convert( input_md )
soup = BeautifulSoup( input_md, 'html.parser' )

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
            new_picture_src1[ 'media' ] = "( min-width: " + my_config[ "break_mid" ] + "px )"
            new_picture_src1[ 'srcset' ] = picture_src
            new_picture_entity_parent.insert( 1, new_picture_src1 )
        else:
            new_picture_src2 = soup.new_tag( 'source' )
            new_picture_src2[ 'media' ] = "( min-width: " + my_config[ "break_min" ] + "px )"
            new_picture_src2[ 'srcset' ] = picture_src
            new_picture_entity_parent.insert( 1, new_picture_src2 )
        i = i + 1
    soup = str( soup ).replace( "</source>", "" ) # it's dirty but we've already performed our transformations
# print( soup )

body = soup + '\n' # I like to have a new line at the end of all my html documents
# body = body.replace( "<body><html><head></head><body>", "" )
head = open( my_config[ "input_folder" ] + my_config[ "assets_folder" ] + my_config[ "tpl_folder" ] + my_config[ "tpl_head" ], 'r' ).read()
head = head.replace( "$title", title_entity )
head = head.replace( "$css", my_config[ "input_folder" ] + my_config[ "assets_folder" ] + my_config[ "css_folder" ] + my_config[ "css_file" ] )
head = head.replace( "$js", my_config[ "js_file" ] )

aside = open( my_config[ "input_folder" ] + my_config[ "assets_folder" ] + my_config[ "tpl_folder" ] + my_config[ "tpl_aside" ], 'r' ).read()
foot = open( my_config[ "input_folder" ] + my_config[ "assets_folder" ] + my_config[ "tpl_folder" ] + my_config[ "tpl_footer" ], 'r' ).read()

# githistory( "documents/index.md" ) # this is where we get our document history from

# check for css
new_css_folder = my_config[ "output_folder" ] + my_config[ "css_folder" ]
css_items = os.listdir( my_config[ "input_folder" ] + my_config[ "assets_folder" ] + my_config[ "css_folder" ] )

i = 0
for css_item in css_items:
    if css_item.lower().endswith( ".css" ):
        i = i + 1
        if i > 0:
            if not os.path.exists( new_css_folder ):
                os.makedirs( new_css_folder )
            shutil.copy2( my_config[ "input_folder" ] + my_config[ "assets_folder" ] + my_config[ "css_folder" ] + css_item, new_css_folder )

output_file = open( my_config[ "output_file" ], 'w' )
output_file.write( head )
output_file.write( '\n' )
output_file.write( my_config[ "output_string" ] )
output_file.write( '\n' )
output_file.write( "<body>" )
output_file.write( body )
output_file.write( '\n' )
output_file.write( aside )
output_file.write( "</body>" )
output_file.write( '\n' )
output_file.write( foot )
output_file.close()
