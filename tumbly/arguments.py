import argparse

# Init and set argparse


def init_argparse():
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
    if args.start:
        offset = args.start
    else:
        offset = 0

    return(username, number, offset)
