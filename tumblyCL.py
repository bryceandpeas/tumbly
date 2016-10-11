import os
import sys
import logging.config

from tumbly.database import create_check_database
from tumbly.scrape import scrape_tumblr
from tumbly.download import download_images
from tumbly.arguments import init_argparse

''' Run '''


def main():

    # Init argparse
    username, number, offset = init_argparse()

    logging.config.fileConfig('./config/log.ini', defaults={'logfilename': 'tumblyCL'})
    log = logging.getLogger(__name__)

    # Init variables

    database_name = ''
    number_to_scrape = ''
    start_offset = ''
    url_to_scrape = ''

    # Get user input
    # Create URL
    url_to_scrape = 'http://{0}.tumblr.com'.format(username)
    log.info('Will scrape: {0}'.format(url_to_scrape))
    # Create database name
    database_name = '{0}.db'.format(username)
    log.info('Will save to: {0} database (SQLite3)'.format(database_name))
    # Check if directory exists, create if not
    script_directory = os.path.dirname(os.path.abspath(__file__))
    downloaded_image_directory = os.path.join(script_directory,
                                              'images',
                                              '{0}_saved_images'
                                              .format(username))

    log.info('Will download images to: {0}'.format(downloaded_image_directory))
    if not os.path.exists(downloaded_image_directory):
        os.makedirs(downloaded_image_directory)
    # Get how many images the user wants to scrape
    number_to_scrape = number
    # If there is a third argument, set the offset
    if len(sys.argv) >= 4:
        start_offset = offset  # noqa
    else:
        start_offset = 0  # noqa

    create_check_database(database_name)

    scrape_tumblr(username,
                  url_to_scrape,
                  database_name,
                  number_to_scrape,
                  offset,
                  limit=20,
                  url_type='blog')

    download_images(username,
                    database_name,
                    downloaded_image_directory,
                    number_to_scrape)

if __name__ == '__main__':
    main()
