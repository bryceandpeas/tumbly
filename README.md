# Tumbly

A tool to download tagged images from tumblr, add their urls and other associated data (tags etc.) to a database.

## Installation

Download the repo.

## Usage
Swap out 'APP KEY HERE' and 'APP SECRET HERE' for your consumer key and consumer secret:

```authorization = tumblpy.Tumblpy(app_key = 'APP KEY HERE',
						app_secret = 'APP SECRET HERE')```

Run the script with your arguments:

```python tumbly.py twitterthecomic 10```
		
(Required) 1: The tumblr username e.g. 'twitterthecomic' from 'twitterthecomic.tumblr.com'
(Required) 2: The number of images to download
(Optional) 3: Offset (what number post to scrape from), the default is 0.

A databse will be created in the working directory alongside a folder to contain the downloaded images.

Each downloaded image's filename will be the tumblr username and an incremented number.

Currently does not support posts with multiple images and will ignore posts without tags.
		
## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request!


