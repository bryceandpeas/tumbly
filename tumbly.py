from itertools import product
import os
from os.path import exists 
import sqlite3
import sys
import urllib.request

import tumblpy

''' Init '''

# Init necessaries
database_name = ''
number_to_scrape = ''
start_offset = ''
url_to_scrape = ''

# Get user input
	# Create URL
url_to_scrape='http://{0}.tumblr.com'.format(sys.argv[1])
print ('Will scrape: {0}'.format(url_to_scrape))
	#Create database name
database_name = '{0}.db'.format(sys.argv[1])
print ('Will save to: {0} database (SQLite3)'.format(database_name))
	# Check if directory exists, create if not
script_directory = os.path.dirname(os.path.abspath(__file__))
downloaded_image_directory = os.path.join(script_directory,'{0}_saved_images'.format(sys.argv[1]))
print('Will download images to: {0}'.format(downloaded_image_directory))
if not os.path.exists(downloaded_image_directory):
	os.makedirs(downloaded_image_directory)
	# Get how many images the user wants to scrape
number_to_scrape = int(sys.argv[2])
	# If there is a third argument, set the offset
if len(sys.argv) >= 4:
   start_offset = int(sys.argv[3])
else :
   start_offset = 0

''' Database Functions '''

# Check database exists, if not, create it and necessary table etc.
def create_check_database(database_name):
    if not exists(database_name):
        # Create the database
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        # Create table for tags, photos and photo tags
        c.execute('''CREATE TABLE IF NOT EXISTS tags
                  (tag_id integer primary key autoincrement, 
                   tag text,
                   unique(tag))''')
        c.execute('''CREATE TABLE IF NOT EXISTS photos
                  (photo_id integer primary key autoincrement, 
                   note_count integer, 
                   url text,
                   unique(url))''')
        c.execute('''CREATE TABLE IF NOT EXISTS photo_tags
                  (tag_id integer, 
                   photo_id integer,
                   unique (tag_id, photo_id),
                   foreign key(tag_id) references tags(tag_id),
                   foreign key(photo_id) references photos(photo_id))''')
        conn.commit()
        return conn
    else:
    	# If it exists connect
        return sqlite3.connect(database_name)

# Functions to call to insert data into database tables      
def add_tags(c, tags, verbose=None):
    c.executemany('''INSERT INTO tags (tag)
                     SELECT * FROM (SELECT ?)
                     WHERE NOT EXISTS 
                     			   (SELECT * FROM tags WHERE tag = ?) 
                     LIMIT 1''', [(t,t) for t in tags]
                     )

def add_photo(c, url, note_count, verbose=None):
    c.execute('''INSERT INTO photos (url, note_count)
                 SELECT * FROM (SELECT ?, ?)
                 WHERE NOT EXISTS (
                   SELECT * FROM photos WHERE url = ?
                 ) LIMIT 1''', (url, note_count, url))

def link_tags_photo(c, tags, url, verbose=None):
    photo_id = c.execute('''SELECT photo_id from photos 
                            where url = ? LIMIT 1''', 
                         (url,)).fetchone()[0]
    tag_ids = [ c.execute('''SELECT tag_id from tags 
                             where tag = ? LIMIT 1''', (t,)).fetchone()[0]
                for t in tags ]
    if verbose : 
       for tag_id, photo_id  in product(tags,[url]):
            print ("#%s %s" % (tag_id, photo_id))
    data = [(photo_id,t,photo_id,t) for t in tag_ids]
    c.executemany('''INSERT INTO photo_tags (photo_id, tag_id)
                     SELECT * FROM (SELECT ?, ?)
                     WHERE NOT EXISTS (
                       SELECT * FROM photo_tags
                         WHERE photo_id = ?
                         AND   tag_id = ?
                     ) LIMIT 1''', data)

''' Scraping functions '''

def scrape_tumblr(url_to_scrape, database_name, number_to_scrape, start_offset=0, limit=20, url_type='blog'):
	# Set authorization
	authorization = tumblpy.Tumblpy(app_key = 'APP KEY HERE',
						app_secret = 'APP SECRET HERE')

	# Connect to database
	print('Connecting to {0}'.format(database_name))
	conn = sqlite3.connect(database_name)
	c = conn.cursor()
	# Start scraping
	print('Scraping : {0}'.format(url_to_scrape))
	number_found = 0
	post_count = 0
	while number_found < number_to_scrape :
		# Get tumblr posts
		print('Checking posts: {0} : {1}'.format(post_count * limit + start_offset, (1 + post_count) * limit + start_offset))

		#Check url is correct, authorize
		if url_type == 'blog':
		   posts = authorization.get('posts', blog_url = url_to_scrape, params = {'limit':limit, 'offset':post_count * limit + start_offset})
		post_count += 1

		for p in posts['posts']:
		  # Check for posts that don't have a photo and skip
		  if(not('photos' in  p)): continue
		  # Check for posts that have multiple photos and skip
		  if(len(p['photos']) != 1): continue
		  # Check for posts that don't have tags and skip
		  if(len(p['tags']) == 0): continue
		  # If we made it through that, we have a new photo
		  number_found += 1

		  # Set scraped info
		  note_count = p['note_count']
		  tags = [ y.strip().lower() for x in p['tags']
									 for y in x.split('\n') ]
		  image_url = p['photos'][0]['original_size']['url']
		  
		  print('Image Found at: {0}, Image number: {1}, Tags are: {2} {3}'.format(sys.argv[1], number_found, image_url,'#' + ' #'.join(tags)))

		  # Add scraped data to database
		  add_tags(c, tags)
		  add_photo(c, image_url, note_count)
		  link_tags_photo(c, tags, image_url)

		  conn.commit()
	conn.close()

''' Downloading Functions '''

def download_images(database_name, downloaded_image_directory, number_to_scrape):
	# Connect to database
	con = sqlite3.connect(database_name)

	with con:    
		# Get image urls from photos table
		cur = con.cursor()    
		cur.execute("SELECT url FROM photos")

		# Init J
		j = 0
		while j < number_to_scrape:
			for url in cur:    
				for i in url:
					print('Image url: ' + i)
					os.chdir(downloaded_image_directory)
					image_name = (sys.argv[1] + '_' + str(j) + '.jpg')
					urllib.request.urlretrieve(i, image_name)
					print ('Downloaded: {0}'.format(image_name))
					j += 1

		print('Finished scraping and downloading')

''' Run '''
# (Fix long argument passing - named tuples or classes?)
def main(database_name, downloaded_image_directory, url_to_scrape, number_to_scrape, start_offset=0, limit=20, url_type='blog'):
	create_check_database(database_name)
	scrape_tumblr(url_to_scrape, database_name, number_to_scrape, start_offset=0, limit=20, url_type='blog')
	download_images(database_name, downloaded_image_directory, number_to_scrape)

if __name__ == '__main__' :
	main(database_name, downloaded_image_directory, url_to_scrape, number_to_scrape, start_offset=0, limit=20, url_type='blog')
