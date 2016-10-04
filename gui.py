import argparse
from itertools import product
import os
import sqlite3
import sys

from database import create_check_database
from scrape import scrape_tumblr
from download import download_images

# Better way for lots of imports other than import * ?
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QBrush, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QDesktopWidget, QGridLayout, QInputDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QSizePolicy, QSpinBox, QTextEdit, QWidget

class Tumbly(QWidget):
    def __init__(self, parent = None):
        super(Tumbly, self).__init__(parent)

        QWidget.__init__(self)

        # Create get images button
        self.generate_password_button = QPushButton('Get images')
        self.generate_password_button.setStyleSheet('font: 12px; background-color:#FFFFFF; border: 1px solid #272727')

        # Create layout, add widgets
        self.grid = QGridLayout()
        # Add widget to row, label to same row, next column
        
        self.grid.addWidget(self.generate_password_button, 5, 2)
        
        # Set layout
        self.setLayout(self.grid)

        # Connect password generate button to password generate functions
        self.generate_password_button.clicked.connect(self.get_images)

        # Set window
        self.setFixedSize(500, 250)
        self.setWindowTitle('tumbly')
        self.setWindowIcon(QIcon(''))
        self.setStyleSheet('background: #FFFFFF')

    def get_images():

        # Init variables
        database_name = ''
        number_to_scrape = ''
        start_offset = ''
        url_to_scrape = ''
        
        username = everylittledefectgetsrespect
        number = 10

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
        

# The usual
def main():
    app = QApplication(sys.argv)

    ex = Tumbly()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
