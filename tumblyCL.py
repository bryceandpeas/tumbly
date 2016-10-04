import argparse
from itertools import product
import os
import sqlite3
import sys

from tumbly.database import create_check_database
from tumbly.scrape import scrape_tumblr
from tumbly.download import download_images

import tumblpy


''' Run '''


def main():

    # Init argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-u',
                        '--username',
                        type=str,
                        help='The username of the tumblr user whos '
                             'tumblr you wish to scrape.',
                        required=True)

    parser.add_argument('-n',
                        '--number',
                        type=int,
                        help='The number of images to scrape.',
                        required=True)

    parser.add_argument('-o',
                        '--start',
                        type=int,
                        help='Post number to start from (offset).',
                        required=False)

    args = parser.parse_args()

    # Set argument variables

    username = args.username
    number = args.number
    offset = args.start

    # Init variables

    database_name = ''
    number_to_scrape = ''
    start_offset = ''
    url_to_scrape = ''

    # Get user input
    # Create URL
    url_to_scrape = 'http://{0}.tumblr.com'.format(username)
    print ('Will scrape: {0}'.format(url_to_scrape))
    # Create database name
    database_name = '{0}.db'.format(username)
    print ('Will save to: {0} database (SQLite3)'.format(database_name))
    # Check if directory exists, create if not
    script_directory = os.path.dirname(os.path.abspath(__file__))
    downloaded_image_directory = os.path.join(script_directory,
                                              '{0}_saved_images'
                                              .format(username))

    print('Will download images to: {0}'.format(downloaded_image_directory))
    if not os.path.exists(downloaded_image_directory):
        os.makedirs(downloaded_image_directory)
    # Get how many images the user wants to scrape
    number_to_scrape = number
    # If there is a third argument, set the offset
    if len(sys.argv) >= 4:
        start_offset = offset
    else:
        start_offset = 0

    create_check_database(database_name)

    scrape_tumblr(url_to_scrape,
                  database_name,
                  number_to_scrape,
                  start_offset=0,
                  limit=20,
                  url_type='blog')

    download_images(username,
                    database_name,
                    downloaded_image_directory,
                    number_to_scrape)

if __name__ == '__main__':
    main()
