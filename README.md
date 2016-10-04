# Tumbly

A tool to download tagged images from tumblr as well as add their urls and other associated data (tags etc.) to a database.

## Installation

Get [tumblpy](https://github.com/michaelhelmick/python-tumblpy)

    pip install python-tumblpy

Download the repo.

## Usage


Swap out 'APP KEY HERE' and 'APP SECRET HERE' for your [consumer key and consumer secret](https://www.tumblr.com/docs/en/api/v2) in ```scrape.py```:

    authorization = tumblpy.Tumblpy(app_key = 'APP KEY HERE',
					    	app_secret = 'APP SECRET HERE')


Run the script with your arguments:

    python tumbly.py -u -n -o
    
    usage: tumbly.py [-h] -u USERNAME -n NUMBER [-o START]

        arguments:
            -h, --help   show this help message and exit
        
            -u USERNAME, --username USERNAME
                         The username of the tumblr user whos tumblr you wish to scrape.
                     
            -n NUMBER,   --number NUMBER
                         The number of images to scrape.
                     
            -o START,    --start START
                         Post number to start from (offset).
		
- Required -u: ```The tumblr username e.g. 'twitterthecomic' from 'twitterthecomic.tumblr.com'.```
- Required -n: ```The number of images to download.```
- Optional -o: ```Offset (what number post to scrape from), the default is 0.```


For example:

    python tumbly.py -u twitterthecomic -n 10

A databse will be created in the working directory alongside a folder to contain the downloaded images.

Each downloaded image's filename will be the tumblr username and an incremented number.

Currently does not support posts with multiple images and will ignore posts without tags.
		
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request!


