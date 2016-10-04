import os
import sqlite3
import sys
import queue

from tumbly.database import create_check_database
from tumbly.scrape import scrape_tumblr
from tumbly.download import download_images

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread
from PyQt5.QtGui import QBrush, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox, QDesktopWidget
from PyQt5.QtWidgets import QGridLayout, QInputDialog, QLabel, QLineEdit
from PyQt5.QtWidgets import QMessageBox, QPushButton, QSizePolicy, QSpinBox
from PyQt5.QtWidgets import QTextEdit, QWidget


class WriteStream(object):
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

    # Everyone loves a no-op
    def flush(self):
        pass


class MyReceiver(QObject):
    mysignal = pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)


class RunMain(QObject):
    @pyqtSlot()
    def run(self, username, number, offset):

        # Init variables
        database_name = ''
        url_to_scrape = ''
        offset = 20
        
        # Get user input
        # Create URL
        url_to_scrape = 'http://{0}.tumblr.com'.format(username)
        # print('Will scrape: {0}'.format(url_to_scrape))
        # Create database name
        database_name = '{0}.db'.format(username)
        # print('Will save to: {0} database (SQLite3)'.format(database_name))
        # Check if directory exists, create if not
        script_directory = os.path.dirname(os.path.abspath(__file__))
        downloaded_image_directory = os.path.join(script_directory,
                                                  '{0}_saved_images'
                                                  .format(username))

        # print('Will download images to: {0}'
        #      .format(downloaded_image_directory))

        if not os.path.exists(downloaded_image_directory):
            os.makedirs(downloaded_image_directory)

        create_check_database(database_name)
        
        scrape_tumblr(username,
                      url_to_scrape,
                      database_name,
                      number,
                      offset=20,
                      limit=20,
                      url_type='blog')

        download_images(username,
                        database_name,
                        downloaded_image_directory,
                        number)

        sys.exit()


class Tumbly(QWidget):
    def __init__(self, parent=None):
        super(Tumbly, self).__init__(parent)

        QWidget.__init__(self)

        # Call functions to create GUI
        self.create_ui()

    def create_ui(self):

        self.username = ''
        self.number = 1
        self.offest = 0

        # Create Labels
        self.number_label = QLabel('Number of images to scrape:')
        self.offset_label = QLabel('Post offest (start point):')

        self.status_out = QTextEdit()
        self.status_out.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Expanding)

        # Create input boxes
        self.username_box = QLineEdit(self)
        self.username_box.setText('Enter username to scrape')
        self.username_box.setSizePolicy(QSizePolicy.Preferred,
                                        QSizePolicy.Expanding)
        self.username_box.textChanged[str].connect(self.text_changed)

        # Create number boxes
        self.number_of_images = QSpinBox()
        self.number_of_images.setMinimum(1)

        self.post_offset = QSpinBox()
        self.post_offset.setMinimum(0)

        # Create get images button
        self.get_button = QPushButton('Get images')
        self.get_button.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Expanding)
        self.get_button.setStyleSheet('font: 12px;'
                                      ' background-color:#FFFFFF;'
                                      ' border: 1px solid #272727')

        # Create layout, add widgets
        self.grid = QGridLayout()
        self.grid.addWidget(self.username_box, 1, 0, 1, 2)
        self.grid.addWidget(self.get_button, 2, 0, 1, 2)
        self.grid.addWidget(self.number_label, 3, 0)
        self.grid.addWidget(self.offset_label, 3, 1)
        self.grid.addWidget(self.number_of_images, 4, 0)
        self.grid.addWidget(self.post_offset, 4, 1)
        self.grid.addWidget(self.status_out, 5, 0, 5, 2)

        # Set layout
        self.setLayout(self.grid)

        self.number = self.number_of_images.value()
        self.offset = self.post_offset.value()

        # Connect get images button to get_images function
        self.get_button.clicked.connect(self.start_thread(self.username,
                                                          self.number,
                                                          self.offset))

        # Set window
        self.setFixedSize(500, 250)
        self.setWindowTitle('tumbly')
        self.setWindowIcon(QIcon(''))
        self.setStyleSheet('background: #FFFFFF')

    def text_changed(self, text):
        # Get text changes
        self.username = str(text)

    @pyqtSlot(str)
    def append_text(self, text):
        self.status_out.moveCursor(QTextCursor.End)
        self.status_out.insertPlainText(text)

    @pyqtSlot()
    def start_thread(self, username, number, offset):

        self.thread = QThread()
        self.run_main = RunMain()
        self.run_main.moveToThread(self.thread)
        self.thread.started.connect(self.run_main.run(username,
                                                      number,
                                                      offset))
        self.thread.start()

queue = queue.Queue()
sys.stdout = WriteStream(queue)


def main():

    app = QApplication(sys.argv)

    ex = Tumbly()
    ex.show()
    sys.exit(app.exec_())

    thread = QThread()
    my_receiver = MyReceiver(queue)
    my_receiver.mysignal.connect(app.append_text)
    my_receiver.moveToThread(thread)
    thread.started.connect(my_receiver.run)
    thread.start()

    qapp.exec_()

if __name__ == '__main__':
    main()
