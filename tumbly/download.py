import sqlite3
import os
import urllib.request
import logging.config
from os.path import join
from tumbly.arguments import init_argparse


''' Downloading Functions '''

BASE_PATH = 'databases'


def download_images(username,
                    database_name,
                    downloaded_image_directory,
                    number):

    # Update database path
    database_path = join(BASE_PATH, database_name)
    # Connect to database
    con = sqlite3.connect(database_path)

    logging.config.fileConfig('./config/log.ini', defaults={'logfilename': 'download'})
    log = logging.getLogger('download')

    # Default number
    if number is None:
        number = 1

    with con:
        # Get image urls from photos table
        cur = con.cursor()
        cur.execute("SELECT url FROM photos")

        # Init J
        j = 0
        while j < number:
            for url in cur:
                if(j < number):
                    for i in url:
                        log.debug('Image url: ' + i)
                        os.chdir(downloaded_image_directory)
                        image_name = (username + '_' + str(j) + '.jpg')
                        urllib.request.urlretrieve(i, image_name)
                        log.debug('Downloaded: {0}'.format(image_name))
                        j += 1

        log.info('Finished scraping and downloading')


def main():

    username, number, offset = init_argparse()

if __name__ == '__main__':
    main()
