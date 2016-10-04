import sqlite3
import sys
import os
import urllib.request

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