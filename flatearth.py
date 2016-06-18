#!/usr/bin/env python

from __future__ import print_function

import os, markdown, shutil

from bs4 import BeautifulSoup
from gittools import githead, gitorigin, githistory
from config import getconfig # this is from config.py - feed it the ini_file string and it will return config with named keys - eg: config[ "your_config_parameter" ]

ini_file = "general.ini"

config = getconfig( ini_file )
backup_config = config # this is so we can reload the config file and still have access to the original values if they're absent from the other ini files

md_items = os.listdir( config[ "document_folder" ] )
for md_item in md_items:
    if md_item.lower().endswith( '.md' ):
        input_md = md_item

md = markdown.Markdown( output_format = "html5" )

input_md = config[ "document_folder" ] + input_md
loc_input_md = input_md
input_md = open( input_md, 'r' ).read()
input_md = md.convert( input_md )
sanitise_md = str( input_md ).replace( ">\n", ">" ) # this is so we can just ignore the extra sibling nodes happen after closing tags
soup = BeautifulSoup( sanitise_md, 'html5lib' )

for html_elem in soup.find_all( 'h1' ):
    title_entity = html_elem.text
for gallery in soup.find_all( 'h3' ):
    if ( gallery.text.lower() == "gallery" ):
        gallery_header = gallery
        gallery_header_next_sibling = gallery_header.next_sibling
        if ( gallery_header.next_sibling.name == "p" ):
            if not ( gallery_header.next_sibling.text == "" ):
                new_gallery_header = soup.new_tag( 'h3' )
                new_gallery_header.string = gallery_header.next_sibling.text
                gallery_header.next_sibling.decompose()
                gallery_header.replaceWith( new_gallery_header )
                gallery_header_next_sibling = new_gallery_header.next_sibling
        i = 0
        for gallery_elem in gallery_header_next_sibling:
            if ( gallery_elem.name.lower() == 'img' ):
                if ( i == 0 ):
                    gallery_elems = {}
                    new_gallery = soup.new_tag( "div" )
                    new_gallery[ "class" ] = "gallery"
                gallery_elems[ i ] = gallery_elem
                new_gallery_elem = soup.new_tag( "figure" )

                if ( gallery_elem.has_attr( "alt" ) ):
                    new_gallery_cap = soup.new_tag( "figcaption" )
                    new_gallery_cap.string = gallery_elem[ "alt" ] # becaue the alt tag should be descriptive of the image we're going to use it as the tag
                    new_gallery_elem.insert( 2, new_gallery_cap )

                if ( gallery_elem.has_attr( "title" ) ):
                    new_gallery_attribution = soup.new_tag( "dl" )
                    new_gallery_attribution_dt = soup.new_tag( "dt" )
                    new_gallery_attribution_dt.string = "Image owner:"
                    new_gallery_attribution_dd = soup.new_tag( "dd" )
                    new_gallery_attribution_dd.string = gallery_elem[ "title" ]
                    new_gallery_attribution.insert( 0, new_gallery_attribution_dt )
                    new_gallery_attribution.insert( 1, new_gallery_attribution_dd )
                    new_gallery_elem.insert( 1, new_gallery_attribution )
                i = i + 1
                new_gallery_elem.insert( 1, gallery_elem )
                # new_gallery.insert( 1, new_gallery_elem )
        gallery_elem.decompose()
        print( gallery_elems )
        try:
            new_gallery_header.insert_after( new_gallery )
        except:
            gallery_header.insert_after( new_gallery )
        gallery_header_next_sibling.decompose()

body = str( soup ) + '\n' # I like to have a new line at the end of all my html documents
# since we have changed to the html5lib it 'helpfully' adds the the html and head elements to the soup which we can get rid of with a string replace
body = body.replace( "<html><head></head><body>", "" )
body = body.replace( "</body></html>", "" )
body = body.replace( "&amp;", "&" ) # thanks bs4 for your escaping of my html-safe characters
# end of string manipulations
head = open( config[ "tpl_head" ], 'r' ).read()
head = head.replace( "$title", title_entity )
head = head.replace( "$css", config[ "css_folder" ] + config[ "css_file" ] )
head = head.replace( "$js", config[ "js_file" ] )

aside = open( config[ "tpl_aside" ], 'r' ).read()

soup = BeautifulSoup( aside, 'html5lib' )

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
    git_url = origin_location.replace( ".git", "" ).replace( "(fetch)", "" ).rstrip()

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
    revision_list.insert( 1, list_item )

# print( soup )

aside = str( soup )
# string manipulations
aside = aside.replace( "<html><head></head><body>", "" )
aside = aside.replace( "</body></html>", "" )
# end of string manipulations

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
