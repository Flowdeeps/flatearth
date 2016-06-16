#!/usr/bin/env python

from __future__ import print_function

import os, markdown, shutil

from bs4 import BeautifulSoup
from gittools import githead, gitorigin, githistory
from config import getconfig # this is from config.py - feed it the ini_file string and it will return config with named keys - eg: config[ "your_config_parameter" ]

ini_file = "general.ini"

config = getconfig( ini_file )

md_items = os.listdir( config[ "document_folder" ] )
for md_item in md_items:
    if md_item.lower().endswith( '.md' ):
        input_md = md_item

md = markdown.Markdown( output_format = "html5" )

input_md = config[ "document_folder" ] + input_md
loc_input_md = input_md
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
            new_picture_src1[ 'media' ] = "( min-width: " + config[ "break_mid" ] + "px )"
            new_picture_src1[ 'srcset' ] = picture_src
            new_picture_entity_parent.insert( i, new_picture_src1 )
        else:
            new_picture_src2 = soup.new_tag( 'source' )
            new_picture_src2[ 'media' ] = "( min-width: " + config[ "break_min" ] + "px )"
            new_picture_src2[ 'srcset' ] = picture_src
            new_picture_entity_parent.insert( i, new_picture_src2 )
        i = i + 1
    soup = str( soup ).replace( "</source>", "" ) # it's dirty but we've already performed our transformations

body = soup + '\n' # I like to have a new line at the end of all my html documents
head = open( config[ "tpl_head" ], 'r' ).read()
head = head.replace( "$title", title_entity )
head = head.replace( "$css", config[ "css_folder" ] + config[ "css_file" ] )
head = head.replace( "$js", config[ "js_file" ] )

aside = open( config[ "tpl_aside" ], 'r' ).read()

soup = BeautifulSoup( aside, 'html.parser' )

# git functions lists and variables
history = githistory( loc_input_md )
current_revision = githead()
origin_details = gitorigin()[ 0 ]
origin_details = origin_details.split( "\t" )
origin_name = origin_details[ 0 ]
origin_location = origin_details[ 1 ]
if "@" in origin_location:
    origin_location = origin_location.split( "@" )
    del origin_location[ 0 ]
    origin_location = origin_location[ 0 ].split( ":" )
    origin_user = origin_location[ 1 ].split( "/" )
    origin_project = origin_user[ 1 ].replace( ".git", "" ).replace( "(fetch)", "" ).rstrip()
    origin_user = origin_user[ 0 ]
    git_url = "https://" + origin_location[ 0 ] + "/" + origin_user + "/" + origin_project
else:
    origin_location = None
# print( origin_name )
# print( origin_location )


for html_elem in soup.find_all( 'ol' ):
    revision_list = html_elem

# create a dl for the current revision
current_rev_dl = soup.new_tag( 'dl' )
current_rev_dt = soup.new_tag( 'dt')
current_rev_dt.string = "Current file version:"
current_rev_dd = soup.new_tag( 'dd' )
current_rev_dd.string = current_revision
current_rev_dl.insert( 1, current_rev_dt)
current_rev_dl.insert( 1, current_rev_dd)
revision_list.insert_before( current_rev_dl )

for revision in history:
    list_item = soup.new_tag( 'li' )
    for data in revision:
        if data.lower().startswith( "commit" ):
            data = data.replace( "commit", "" ).lstrip()
            data_elem = soup.new_tag( 'a' )
            data_elem[ "target" ] = "_blank"
            data_elem[ "rel" ] = "external"
            data_elem.string = data
            data_elem[ 'href' ] = git_url + "/commit/" + data + "#diff-" + current_revision
        else:
            data_elem = soup.new_tag( 'div' )
            data_elem.string = data
        list_item.insert( 1, data_elem )
    revision_list.insert( i, list_item )

# print( soup )

aside = str( soup )

foot = open( config[ "tpl_footer" ], 'r' ).read()

# check for css
new_css_folder = config[ "output_folder" ] + config[ "css_folder" ]
css_items = os.listdir( config[ "input_folder" ] + config[ "assets_folder" ] + config[ "css_folder" ] )

i = 0
for css_item in css_items:
    if css_item.lower().endswith( ".css" ):
        i = i + 1
        if i > 0:
            if not os.path.exists( new_css_folder ):
                os.makedirs( new_css_folder )
            shutil.copy2( config[ "input_folder" ] + config[ "assets_folder" ] + config[ "css_folder" ] + css_item, new_css_folder )

output_file = open( config[ "output_folder" ] + config[ "output_file" ], 'w' )
output_file.write( head )
output_file.write( '\n' )
output_file.write( config[ "output_string" ] )
output_file.write( '\n' )
output_file.write( "<body>" )
output_file.write( body )
output_file.write( '\n' )
output_file.write( aside )
output_file.write( "</body>" )
output_file.write( '\n' )
output_file.write( foot )
output_file.close()
