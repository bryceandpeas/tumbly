from itertools import product
import os
import sqlite3
import sys

from database import create_check_database
from scrape import scrape_tumblr
from download import download_images

import tumblpy

''' Run '''

# (Fix long argument passing - named tuples or classes?)


def main(database_name,
         downloaded_image_directory,
         url_to_scrape,
         number_to_scrape,
         start_offset=0,
         limit=20,
         url_type='blog'):

    create_check_database(database_name)

    scrape_tumblr(url_to_scrape,
                  database_name,
                  number_to_scrape,
                  start_offset=0,
                  limit=20,
                  url_type='blog')

    download_images(database_name,
                    downloaded_image_directory,
                    number_to_scrape)

if __name__ == '__main__':

    ''' Init '''

    # Init variables
    database_name = ''
    number_to_scrape = ''
    start_offset = ''
    url_to_scrape = ''

    # Get user input
    # Create URL
    url_to_scrape = 'http://{0}.tumblr.com'.format(sys.argv[1])
    print ('Will scrape: {0}'.format(url_to_scrape))
    # Create database name
    database_name = '{0}.db'.format(sys.argv[1])
    print ('Will save to: {0} database (SQLite3)'.format(database_name))
    # Check if directory exists, create if not
    script_directory = os.path.dirname(os.path.abspath(__file__))
    downloaded_image_directory = os.path.join(script_directory,
                                              '{0}_saved_images'
                                              .format(sys.argv[1]))

    print('Will download images to: {0}'.format(downloaded_image_directory))
    if not os.path.exists(downloaded_image_directory):
        os.makedirs(downloaded_image_directory)
    # Get how many images the user wants to scrape
    number_to_scrape = int(sys.argv[2])
    # If there is a third argument, set the offset
    if len(sys.argv) >= 4:
        start_offset = int(sys.argv[3])
    else:
        start_offset = 0

    main(database_name,
         downloaded_image_directory,
         url_to_scrape,
         number_to_scrape,
         start_offset=0,
         limit=20,
         url_type='blog')
