# Tumbly [![Build Status](https://travis-ci.org/BryceFury/tumbly.svg?branch=master)](https://travis-ci.org/BryceFury/tumbly) [![codecov](https://codecov.io/gh/BryceFury/tumbly/branch/master/graph/badge.svg)](https://codecov.io/gh/BryceFury/tumbly) [![Code Climate](https://codeclimate.com/repos/57f7356ba06b6a2fa8001247/badges/037f6832825799fa607f/gpa.svg)](https://codeclimate.com/repos/57f7356ba06b6a2fa8001247/feed) [![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)


A tool to download tagged images from tumblr as well as add their urls and other associated data (tags etc.) to a database.


## Contents  
1. [Installation](#installation)

2. [Usage](#usage)
 - [Graphical](#graphical)
 - [Commandline/Terminal](#terminal)
 
3. [Contributing](#contributing)
4. [TO DO](#todo)
4. [Contributors](#contributors)
  
  
## Installation<a name="installation"/>

Get all the necessities:
    
    pip install -r requirements.txt
    
or download individually:

Get [tumblpy](https://github.com/michaelhelmick/python-tumblpy):

    pip install python-tumblpy
    
Get [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)

    pip install pyqt5

Download the repo.


## Usage<a name="usage"/>

### Graphical<a name="graphical"/> (```run.py```)

Run:

    python run.py

Click the 'Set Auth' button and add your [consumer key and consumer secret](https://www.tumblr.com/docs/en/api/v2). 
(You do not need to do this if you have already set them by running ```tumblyCL.py```).
   
Enter the tumblr username, number of images to download and the offset (defaults to 20).

![](https://raw.githubusercontent.com/BryceFury/tumbly/master/assets/screenshots/tumbly_screenshot.png)


### Commandline/Terminal<a name="terminal"/> (```tumblyCL.py```)


Run the script with your arguments:

    python tumblyCL.py -u -n -o
    
***

If this is the first time you have used the script, you will be prompted to add your [consumer key and consumer secret](https://www.tumblr.com/docs/en/api/v2), it will not work otherwise.
(You do not need to do this if you have already set them by running ```run.py```).

***
    usage: tumblyCL.py [-h] -u USERNAME -n NUMBER [-o START]

        arguments:
            -h, --help   show this help message and exit
        
            -u USERNAME, --username USERNAME
                         The username of the tumblr user whose tumblr you wish to scrape.
                     
            -n NUMBER,   --number NUMBER
                         The number of images to scrape.
                     
            -o START,    --start START
                         Post number to start from (offset).
                         
***

- Required -u: ```The tumblr username e.g. 'twitterthecomic' from 'twitterthecomic.tumblr.com'.```
- Required -n: ```The number of images to download.```
- Optional -o: ```Offset (what number post to scrape from), the default is 0.```

***

_Example_:

    python tumblyCL.py -u twitterthecomic -n 10

A databse will be created in the working directory alongside a folder to contain the downloaded images.

Each downloaded image's filename will be the tumblr username and an incremented number.

Currently does not support posts with multiple images and will ignore posts without tags.


## Contributing<a name="contributing"/> 
1. Fork it!
2. Checkout the to do list below or any open issues.
3. Create your feature branch: `git checkout -b my-new-feature`
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request!


## TO DO<a name="todo"/> 

- [X] Code refactoring. > ([#1](https://github.com/BryceFury/tumbly/issues/1))
- [ ] Prettier GUI. > ([#2](https://github.com/BryceFury/tumbly/issues/2))
- [ ] Image viewing functionality for downloaded images. > ([#3](https://github.com/BryceFury/tumbly/issues/3))
- [ ] Unit testing. > ([#4](https://github.com/BryceFury/tumbly/issues/4))
- [ ] Data viewing for downloaded tags, etc. > ([#5](https://github.com/BryceFury/tumbly/issues/5))
- [X] Better filepaths e.g. ../databases/username.db > ([#6](https://github.com/BryceFury/tumbly/issues/6))


## Contributors<a name="contributors"/> 
- [pratyushprakash](https://github.com/pratyushprakash) - Implemented [#6](https://github.com/BryceFury/tumbly/issues/6) in [#7](https://github.com/BryceFury/tumbly/pull/7)

- [Algogator](https://github.com/Algogator) - Fixed [#15](https://github.com/BryceFury/tumbly/pull/15) in [#16](https://github.com/BryceFury/tumbly/pull/16), fixed [#17](https://github.com/BryceFury/tumbly/pull/17) in [#18](https://github.com/BryceFury/tumbly/pull/18) and  fixed [#20](https://github.com/BryceFury/tumbly/pull/20) in [#21](https://github.com/BryceFury/tumbly/pull/21). Contibuted to [#1](https://github.com/BryceFury/tumbly/pull/1).

- [aniketmaithani](https://github.com/aniketmaithani) - Contributed to [#1](https://github.com/BryceFury/tumbly/pull/1) in [#22](https://github.com/BryceFury/tumbly/pull/22)



