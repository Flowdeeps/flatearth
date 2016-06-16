# Flat Earth

 A python-based NoCMS which produces flat HTML sites from Markdown files and directory structure.

## Why?

I spend a lot of my time in the command line so producing content via a repository and git is much quicker and easier than logging into a Wordpress site and editing there. Plus there's the history of the article in the commit messages for transparency.

## TODO
* Get git file history and write into opened aside file - In progress
* Iterate through all folders in documents for markdown files
* Navigation? I didn't even consider that when I started
* Get links for images to process from md, not to go through the documents folder for them - this will save on cycles and we can also then iterate through the output html for each element at the same time, only writing in the necessary picture sources
* Work out what to do with images. Currently I'm looking at ~~imagemagick or gd-image~~ Pillow to convert them to three sizes for a <picture> element (note: this is done now but needs to be abstracted to make it more useful and efficient)
* Add support for galleries and figures/figcaptions etc - my current thoughts are that it will be any images immediately following a ### gallery (Which I think is h3)
* Check if the remote the docs come from are ssh or https then edit the diff link accordingly
* Add support for video and audio - this is not going to be easy but I guess I can do a check for file extension after a !(alt)[url]
* Add githook for pulling changes to a server and running app - I need to research this more

## Setting Up

I've been developing using virtualenv and suggest you do the same whilst the app becomes more stable and the dependencies stop changing.

$pip install virtualenv

$pip install -r requirements.txt

$cd output/

$python flatearth.py

If you have not edited the general.ini then it will generate files for the site in the 'output' folder

## License

MIT
