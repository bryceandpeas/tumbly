import argparse
from itertools import product
import os
import sqlite3
import sys

from tumbly.database import create_check_database
from tumbly.scrape import scrape_tumblr
from tumbly.download import download_images

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QDesktopWidget
from PyQt5.QtWidgets import QGridLayout, QInputDialog, QLabel, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QPushButton, QSizePolicy, QSpinBox
from PyQt5.QtWidgets import QTextEdit, QWidget

class Tumbly(QWidget):
    def __init__(self, parent = None):
        super(Tumbly, self).__init__(parent)

        QWidget.__init__(self)

        self.create_statusbar()
        self.create_ui()

    def create_ui(self):
        # Satusbar welcome
        self.statusbar.showMessage('Welcome to tumbly!')

        # Create Labels
        self.numbers_label = QLabel('Number of images to scrape')

        # Create input boxes
        self.username_box = QLineEdit(self)
        self.username_box.setText('Enter username to scrape')
        self.username_box.textChanged[str].connect(self.text_changed)

        # Create number boxes
        self.number_of_images = QSpinBox()

        # Create get images button
        self.get_button = QPushButton('Get images')
        self.get_button.setStyleSheet('font: 12px;'
                                      ' background-color:#FFFFFF;'
                                      ' border: 1px solid #272727')

        # Create output box
        self.password_output = QTextEdit()
        self.password_output.setReadOnly(True)
        self.password_output.setSizePolicy(QSizePolicy.Preferred, 
                                           QSizePolicy.Expanding)
        self.password_output.setStyleSheet('font: bold 12px;'
                                           'background: #FFFFFF;'
                                           'border: 1px solid #272727')

        # Create layout, add widgets
        self.grid = QGridLayout()
        self.grid.addWidget(self.username_box, 0, 0)
        self.grid.addWidget(self.get_button, 0, 1)
        self.grid.addWidget(self.numbers_label, 1, 0)
        self.grid.addWidget(self.number_of_images, 1, 1)
            
            
        # Set layout
        self.setLayout(self.grid)

        # Connect get images button to get_images function
        self.get_button.clicked.connect(self.get_images)

        # Set window
        self.setFixedSize(500, 250)
        self.setWindowTitle('tumbly')
        self.setWindowIcon(QIcon(''))
        self.setStyleSheet('background: #FFFFFF')   
            

    def create_statusbar(self):
        # Create statusbar
        self.statusbar = QtWidgets.QStatusBar(self)
        
        self.statusbar.setStatusTip('')
        
    def text_changed(self, text):
        self.username = str(text)

    def get_images(self, username):

        # Init variables
        database_name = ''
        number_to_scrape = ''
        start_offset = ''
        url_to_scrape = ''
        
        username = self.username
        # Get how many images the user wants to scrape
        number_to_scrape = self.number_of_images.value()
 
        # Get user input
        # Create URL
        url_to_scrape = 'http://{0}.tumblr.com'.format(username)
        self.statusbar.showMessage('Will scrape: {0}'.format(url_to_scrape))
        # Create database name
        database_name = '{0}.db'.format(username)
        self.statusbar.showMessage('Will save to: {0} database (SQLite3)'.format(database_name))
        # Check if directory exists, create if not
        script_directory = os.path.dirname(os.path.abspath(__file__))
        downloaded_image_directory = os.path.join(script_directory,
                                                  '{0}_saved_images'
                                                  .format(username))

        self.statusbar.showMessage('Will download images to: {0}'.format(downloaded_image_directory))
        if not os.path.exists(downloaded_image_directory):
            os.makedirs(downloaded_image_directory)

        self.statusbar.showMessage('Checking database')
        create_check_database(database_name)
        
        self.statusbar.showMessage('Getting images')
        scrape_tumblr(username,
                      url_to_scrape,
                      database_name,
                      number_to_scrape,
                      start_offset=0,
                      limit=20,
                      url_type='blog')

        self.statusbar.showMessage('Downloading images')
        download_images(username,
                        database_name,
                        downloaded_image_directory,
                        number_to_scrape)

        sys.exit()

    
    
    

    

def main():

    app = QApplication(sys.argv)

    ex = Tumbly()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
