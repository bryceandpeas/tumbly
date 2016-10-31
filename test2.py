# coding=UTF-8

import random
import string
import sys

from tumbly.confighandler import put_config
from tumbly.database import create_check_database
from tumbly.scrape import scrape_tumblr
from tumbly.download import download_images 
from tumbly.stylesheet import set_stylesheet


from PyQt5 import QtCore, QtGui, QtWidgets


# Create main canvas
class Tumbly(QtWidgets.QMainWindow):
 

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self,parent)

        # Call function to create UI
        self.create_main_ui()


    def create_main_ui(self):

        # Set window stylesheet
        get_stylesheet = set_stylesheet()
        self.setStyleSheet(get_stylesheet)

        # Main window setting
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName('centralWidget')

        # Set main widget layout (centralWidget)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(-1)
        self.verticalLayout_10.setObjectName('verticalLayout_10')

         # Create top frame
        self.top_frame = QtWidgets.QFrame(self.centralWidget)
        self.top_frame.setObjectName('top_frame')
        self.horizontallayout_10 = QtWidgets.QHBoxLayout(self.top_frame)
        self.horizontallayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontallayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout_10.setSpacing(0)
        self.horizontallayout_10.setObjectName('horizontallayout_10')

        # Add top frame to layout
        self.verticalLayout_10.addWidget(self.top_frame)
        
        # Create frame for menu button and title
        self.menu_frame = QtWidgets.QFrame(self.top_frame)

        # Set frame size
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu_frame.sizePolicy().hasHeightForWidth())
        self.menu_frame.setSizePolicy(sizePolicy)
        self.menu_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menu_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menu_frame.setObjectName('menu_frame')

        # Set menu frames layout
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.menu_frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName('horizontalLayout')

        # Create menubutton
        self.menu_button = QtWidgets.QPushButton(self.menu_frame)
        self.menu_button.setObjectName('menu_button')
        self.menu_button.setText('☰')

        # Add menubutton widget to layout
        self.horizontalLayout.addWidget(self.menu_button)

        # Connect menu button to open_menu function
        self.menu_button.clicked.connect(self.open_menu)

        # Add menu frame to layout
        self.horizontallayout_10.addWidget(self.menu_frame)

        # Create title label
        self.title_label = QtWidgets.QLabel(self.menu_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_label.sizePolicy().hasHeightForWidth())
        self.title_label.setSizePolicy(sizePolicy)
        self.title_label.setObjectName('title_label')
        self.title_label.setText('tumbly.')

        # Add title label to layout
        self.horizontalLayout.addWidget(self.title_label)

        # Create frame for username input
        self.username_input_frame = QtWidgets.QFrame(self.top_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_input_frame.sizePolicy().hasHeightForWidth())
        self.username_input_frame.setSizePolicy(sizePolicy)
        self.username_input_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.username_input_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.username_input_frame.setObjectName('username_input_frame')

        # Create layout for username input frame
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.username_input_frame)
        self.verticalLayout_3.setContentsMargins(0, 2.5, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        
        # Create username box
        self.username_box = QtWidgets.QLineEdit(self.username_input_frame)
        self.username_box.setText('Enter username to scrape')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_box.sizePolicy().hasHeightForWidth())
        self.username_box.setSizePolicy(sizePolicy)
        self.username_box.setObjectName('username_box')

        # Listen input changes
        self.username_box.textChanged[str].connect(self.text_changed)

        # Add username box layout
        self.verticalLayout_3.addWidget(self.username_box)

        # Add username input frame to layout
        self.horizontallayout_10.addWidget(self.username_input_frame)

        # Create frame for scrape button
        self.scrape_frame = QtWidgets.QFrame(self.top_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrape_frame.sizePolicy().hasHeightForWidth())
        self.scrape_frame.setSizePolicy(sizePolicy)
        self.scrape_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrape_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scrape_frame.setObjectName('scrape_frame')

        # Create layout for scrape button frame
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.scrape_frame)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName('verticalLayout_3')

        # Create scrape button
        self.scrape_button = QtWidgets.QPushButton(self.scrape_frame)
        self.scrape_button.setText('scrape')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrape_button.sizePolicy().hasHeightForWidth())
        self.scrape_button.setSizePolicy(sizePolicy)
        self.scrape_button.setObjectName('scrape_button')

        # Add scrape button to layout
        self.verticalLayout_15.addWidget(self.scrape_button)

        # Add scrape frame to layout
        self.horizontallayout_10.addWidget(self.scrape_frame)

        # Create frame for exit button
        self.exit_frame = QtWidgets.QFrame(self.top_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_frame.sizePolicy().hasHeightForWidth())
        self.exit_frame.setSizePolicy(sizePolicy)
        self.exit_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.exit_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.exit_frame.setObjectName('exit_frame')

        # Create layout for exit button frame
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.exit_frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        
        # Create exit button
        self.exit_button = QtWidgets.QPushButton(self.exit_frame)
        self.exit_button.setText('exit')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(sizePolicy)
        self.exit_button.setObjectName('exit_button')

        # Add exit button to layout
        self.verticalLayout_3.addWidget(self.exit_button)

        # Add exit frame to layout
        self.horizontallayout_10.addWidget(self.exit_frame)

        # Connect exit button to close function
        self.exit_button.clicked.connect(self.close)

        # Connect exit button to close function
        self.scrape_button.clicked.connect(self.scrape)
        
        # Set central widget
        self.setCentralWidget(self.centralWidget)

        # Hide OS' default window title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Call menu ui to set options and immediately hide
        self.menu_ui()
        self.options_frame.hide()

        # Reset menu button icon
        self.menu_button.setText('☰')
        # Reset window size
        self.resize(500, 50)

        # Set password output open flag
        self.password_output_open = False

        # Set menu open flag
        self.menu_open = False


    def menu_ui(self):

        # Set open flag
        self.menu_open = True 

        # Change menu button to 'open'
        self.menu_button.setText('☷')

        # Create options frame
        self.options_frame = QtWidgets.QFrame(self.centralWidget)
        self.options_frame.setObjectName('options_frame')
        self.horizontallayout_4 = QtWidgets.QHBoxLayout(self.options_frame)
        self.horizontallayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontallayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout_4.setSpacing(0)
        self.horizontallayout_4.setObjectName('horizontallayout_4')

        # Add options frame to layout
        self.verticalLayout_10.addWidget(self.options_frame)
        
        # Add options inputs frame        
        self.option_inputs_frame = QtWidgets.QFrame(self.options_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.option_inputs_frame.sizePolicy().hasHeightForWidth())
        self.option_inputs_frame.setSizePolicy(sizePolicy)
        self.option_inputs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.option_inputs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.option_inputs_frame.setObjectName('option_inputs_frame')
        self.horizontallayout_3 = QtWidgets.QHBoxLayout(self.option_inputs_frame)
        self.horizontallayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout_3.setSpacing(0)
        self.horizontallayout_3.setObjectName('horizontallayout_3')
        self.option_inputs_frame = QtWidgets.QFrame(self.option_inputs_frame)
        self.option_inputs_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.option_inputs_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.option_inputs_frame.setObjectName('option_inputs_frame')
        self.verticallayout_6 = QtWidgets.QVBoxLayout(self.option_inputs_frame)
        self.verticallayout_6.setContentsMargins(11, 11, 11, 11)
        self.verticallayout_6.setSpacing(6)
        self.verticallayout_6.setObjectName('verticallayout_6')

        self.key_input = QtWidgets.QLineEdit(self.option_inputs_frame)
        self.key_input.setObjectName('key_input')
        self.verticallayout_6.addWidget(self.key_input)
        self.key_input.setText('Please enter your key')

        self.secret_input = QtWidgets.QLineEdit(self.option_inputs_frame)
        self.secret_input.setObjectName('secret_input')
        self.verticallayout_6.addWidget(self.secret_input)
        self.secret_input.setText('Please enter your secret')

        self.horizontallayout_3.addWidget(self.option_inputs_frame)
        self.case_frame = QtWidgets.QFrame(self.option_inputs_frame)
        self.case_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.case_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.case_frame.setObjectName('case_frame')
        self.verticallayout_7 = QtWidgets.QVBoxLayout(self.case_frame)
        self.verticallayout_7.setContentsMargins(11, 11, 11, 11)
        self.verticallayout_7.setSpacing(6)
        self.verticallayout_7.setObjectName('verticallayout_7')
        self.horizontallayout_3.addWidget(self.case_frame)
        self.horizontallayout_4.addWidget(self.option_inputs_frame)
        self.spins_frame = QtWidgets.QFrame(self.options_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spins_frame.sizePolicy().hasHeightForWidth())     
        
        self.close_button_frame = QtWidgets.QFrame(self.options_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button_frame.sizePolicy().hasHeightForWidth())
        
        self.close_button_frame.setSizePolicy(sizePolicy)
        self.close_button_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.close_button_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.close_button_frame.setObjectName('close_button_frame')
        self.verticallayout_4 = QtWidgets.QVBoxLayout(self.close_button_frame)
        self.verticallayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticallayout_4.setSpacing(0)
        self.verticallayout_4.setObjectName('verticallayout_4')
        self.close_options_button = QtWidgets.QPushButton(self.close_button_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_options_button.sizePolicy().hasHeightForWidth())
        self.close_options_button.setSizePolicy(sizePolicy)
        self.close_options_button.setObjectName('close_options_button')
        self.verticallayout_4.addWidget(self.close_options_button)
        self.horizontallayout_4.addWidget(self.close_button_frame)
                
        self.close_options_button.setText('⇪')

        # Connect options close button to options_close function
        self.close_options_button.clicked.connect(self.close_menu)
    

    def open_menu(self):
        if not self.menu_open:
            self.menu_ui()
        else:
            self.close_menu()


    def close_menu(self):
        
        # Hide menu
        self.options_frame.hide()

        # Reset window size
        self.resize(500, 50)

        # Reset menu button icon
        self.menu_button.setText('☰')

        # Set menu open flag
        self.menu_open = False
    

    ''' Input listening functions '''


    def text_changed(self, text):
        # Get text changes
        self.username = str(text)
        global user_username
        user_username = self.username

    def number_changed(self, number):
        self.number = int(number)
        global user_number
        user_number = self.number

    def offset_changed(self, number):
        self.offset = int(number)
        global user_offset
        user_offset = self.offset


    ''' Tumblr scraping functions '''


    def scrape(self):
        return None

        

    ''' Main window movement functions '''


    def mousePressEvent(self, event):
        self.offset = event.pos()


    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

    
 
''' Run '''


def main():
 
    app = QtWidgets.QApplication(sys.argv)
 
    main = Tumbly()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    
    main()
