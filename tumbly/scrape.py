import argparse
import sqlite3
import sys

from tumbly.database import create_check_database
from tumbly.database import add_tags, add_photo, link_tags_photo

import tumblpy


''' Scraping functions '''


def scrape_tumblr(username,
                  url_to_scrape,
                  database_name,
                  number,
                  offset,
                  limit=20,
                  url_type='blog'):

    # Default offset
    if offset is None or offset == 0:
        offset = 20

    # Default number
    if number is None:
        number = 1

    # Set authorization

    authorization = tumblpy.Tumblpy(app_key='APP KEY HERE',
                                    app_secret='APP SECRET HERE')

    # Connect to database
    print('Connecting to {0}'.format(database_name))
    conn = create_check_database(database_name)
    c = conn.cursor()
    # Start scraping
    print('Scraping : {0}'.format(url_to_scrape))
    number_found = 0
    post_count = 0
    while number_found < number:
        # Get tumblr posts
        print('Checking posts: {0} : {1}'.format(post_count *
                                                 limit +
                                                 offset,
                                                 (1 + post_count) *
                                                 limit + offset))

        # Check url is correct, authorize
        if url_type == 'blog':
            posts = authorization.get('posts',
                                      blog_url=url_to_scrape,
                                      params={'limit': limit,
                                              'offset': int(post_count) *
                                              limit +
                                              offset})

        post_count += 1

        for p in posts['posts']:
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

            print('Image Found at: {2}, '
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

    # Set variables

    username = args.username
    number = args.number
    offset = args.start


if __name__ == '__main__':
    main()
