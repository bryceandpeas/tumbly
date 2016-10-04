import sqlite3
import sys

from database import create_check_database, add_tags, add_photo, link_tags_photo

import tumblpy

''' Scraping functions '''

def scrape_tumblr(url_to_scrape, database_name, number_to_scrape, start_offset=0, limit=20, url_type='blog'):
	# Set authorization
	authorization = tumblpy.Tumblpy(app_key = 'V55FKUe1lMSdx0UyGSFknmO8DoSaeNzT9oByUwOE1Hvp7diQJ7',
						app_secret = 'TD9eTgRhoo8ceu0cjcF0nROWAAMkst1uAkSx5XuSOjnYxrGq50')
	
	#authorization = tumblpy.Tumblpy(app_key = 'APP KEY HERE',
	#					app_secret = 'APP SECRET HERE')

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
		  
		  print('Image Found at: {2}, Image number: {1}, Tags are: {3}'.format(sys.argv[1], number_found, image_url,'#' + ' #'.join(tags)))

		  # Add scraped data to database
		  add_tags(c, tags)
		  add_photo(c, image_url, note_count)
		  link_tags_photo(c, tags, image_url)

		  conn.commit()
	conn.close()
