import os
import sys
import logging.config

from tumbly.confighandler import get_config, put_config
from tumbly.arguments import init_argparse
from tumbly.database import create_check_database
from tumbly.database import add_tags, add_photo, link_tags_photo

import tumblpy

# Get configuration


''' Scraping functions '''


def scrape_tumblr(username,
                  url_to_scrape,
                  database_name,
                  number,
                  offset,
                  limit=20,
                  url_type='blog'):

    def updateconfig():
        while True:
            key = input('Please enter an app key: ')
            if(key == ""):
                continue
            break
        while True:
            secret = input('Please enter an app secret: ')
            if(secret == ""):
                continue
            break
        put_config('config/tumblyconfig.ini', key, secret)
        return (key, secret)

    def getconfig():
        if not os.path.isfile('config/tumblyconfig.ini'):
            print('You do not appear to have a config file'
                  ' let\'s create one')
            key, secret = updateconfig()
            print('config file created')
            return (key, secret)

        else:
            config_pull = get_config('config/tumblyconfig.ini')
            if(str(config_pull[0]) == "" or str(config_pull[1]) == ""):
                app_key, app_secret = updateconfig()
            else:
                app_key = str(config_pull[0])
                app_secret = str(config_pull[1])
            return (app_key, app_secret)

    logging.config.fileConfig('./config/log.ini', defaults={'logfilename': 'scrape'})
    log = logging.getLogger('scrape')

    # Default offset
    if offset is None or offset == 0:
        offset = 20

    # Default number
    if number is None:
        number = 1

    # Set authorization
    app_key, app_secret = getconfig()
    authorization = tumblpy.Tumblpy(app_key=app_key,
                                    app_secret=app_secret)

    # Connect to database
    log.debug('Connecting to {0}'.format(database_name))
    conn = create_check_database(database_name)
    c = conn.cursor()
    # Start scraping
    log.debug('Scraping : {0}'.format(url_to_scrape))
    number_found = 0
    post_count = 0
    while number_found < number:
        # Get tumblr posts
        log.debug('Checking posts: {0} : {1}'.format(post_count *
                                                     limit +
                                                     offset,
                                                     (1 + post_count) *
                                                     limit + offset))

        # Check url is correct, authorize
        if url_type == 'blog':
            posts = None
            try:
                posts = authorization.get('posts',
                                          blog_url=url_to_scrape,
                                          params={'limit': limit,
                                                  'offset': int(post_count) *
                                                  limit +
                                                  offset})
            except tumblpy.TumblpyError as e:
                if e.error_code == 404:
                    log.error("Invalid user")
                else:
                    log.error(e)
            finally:
                sys.exit(0)

        post_count += 1

        for p in posts['posts']:
            if(number_found < number):
                # Check for posts that don't have a photo and skip
                if(not('photos' in p)):
                    continue
                # Check for posts that have multiple photos and skip
                if(len(p['photos']) != 1):
                    continue
                # Check for posts that don't have tags and skip
                if(len(p['tags']) == 0):
                    continue

                number_found += 1

                # Set scraped info
                note_count = p['note_count']
                tags = [y.strip().lower() for x in p['tags']
                        for y in x.split('\n')
                        ]

                image_url = p['photos'][0]['original_size']['url']

                log.debug('Image Found at: {2}, '
                          'Image number: {1}, '
                          'Tags are: {3}'.format(username,
                                                 number_found,
                                                 image_url,
                                                 '#' + ' #'.join(tags)))

                # Add scraped data to database
                add_tags(c, tags)
                add_photo(c, image_url, note_count)
                link_tags_photo(c, tags, image_url)

                conn.commit()
    conn.close()


def main():

    username, number, offset = init_argparse()

if __name__ == '__main__':
    main()
