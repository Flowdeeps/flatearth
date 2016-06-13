# Flat Earth

 A python-based NoCMS which produces flat HTML sites from Markdown files and directory structure.

## Why?

I spend a lot of my time in the command line so producing content via a repository and git is much quicker and easier than logging into a Wordpress site and editing there. Plus there's the history of the article in the commit messages for transparency.

## TODO
* Get git file history and write into opened aside file
* Iterate through all folders in documents for markdown files
* Work out what to do with images. Currently I'm looking at imagemagick or gd-image to convert them to three sizes for a <picture> element
* Add githook for pulling changes to a server and running app

## License

MIT
