# Flat Earth

 A python-based NoCMS which produces flat HTML sites from Markdown files and directory structure.

## Why?

I spend a lot of my time in the command line so producing content via a repository and git is much quicker and easier than logging into a Wordpress site and editing there. Plus there's the history of the article in the commit messages for transparency.

## TODO
* Get git file history and write into opened aside file
* Iterate through all folders in documents for markdown files
* Get links for images to process from md, not to go through the documents folder for them - this will save on cycles and we can also then iterate through the output html for each element at the same time, only writing in the necessary picture sources
* Work out what to do with images. Currently I'm looking at ~~imagemagick or gd-image~~ Pillow ~~to convert them to three sizes for a <picture> element (note: this is done now) ~~
* Add support for galleries and figures/figcaptions etc
* Add support for video and audio
* Add githook for pulling changes to a server and running app

## License

MIT
