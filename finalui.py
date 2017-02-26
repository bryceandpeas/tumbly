# coding=UTF-8

import random
import string
import sys

from stylesheet import set_stylesheet


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
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName('verticalLayout_10')

         # Create top frame
        self.top_frame = QtWidgets.QFrame(self.centralWidget)
        self.top_frame.setObjectName('top_frame')
        self.horizontallayout_10 = QtWidgets.QHBoxLayout(self.top_frame)
        self.horizontallayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontallayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout_10.setSpacing(-1)
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
        self.horizontalLayout.setSpacing(-1)
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
        #self.username_box.textChanged[str].connect(self.text_changed)

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
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

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
       
        self.spins_frame = QtWidgets.QFrame(self.options_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spins_frame.sizePolicy().hasHeightForWidth())

        self.spins_frame.setSizePolicy(sizePolicy)
        self.spins_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.spins_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spins_frame.setObjectName('spins_frame')
        self.verticallayout_3 = QtWidgets.QVBoxLayout(self.spins_frame)
        self.verticallayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticallayout_3.setSpacing(0)
        self.verticallayout_3.setObjectName('verticallayout_3')
        self.labels_frame = QtWidgets.QFrame(self.spins_frame)
        self.labels_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.labels_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labels_frame.setObjectName('labels_frame')
        self.horizontallayout_6 = QtWidgets.QHBoxLayout(self.labels_frame)
        self.horizontallayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout_6.setSpacing(0)
        self.horizontallayout_6.setObjectName('horizontallayout_6')
        self.characters_label_frame = QtWidgets.QFrame(self.labels_frame)
        self.characters_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.characters_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.characters_label_frame.setObjectName('characters_label_frame')
        self.verticallayout_5 = QtWidgets.QVBoxLayout(self.characters_label_frame)
        self.verticallayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticallayout_5.setSpacing(0)
        self.verticallayout_5.setObjectName('verticallayout_5')
        self.characters_label = QtWidgets.QLabel(self.characters_label_frame)
        self.characters_label.setObjectName('characters_label')
        self.verticallayout_5.addWidget(self.characters_label)
        self.horizontallayout_6.addWidget(self.characters_label_frame)
        self.passwords_label_frame = QtWidgets.QFrame(self.labels_frame)
        self.passwords_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.passwords_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.passwords_label_frame.setObjectName('passwords_label_frame')
        self.horizontallayout_7 = QtWidgets.QHBoxLayout(self.passwords_label_frame)
        self.horizontallayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout_7.setSpacing(0)
        self.horizontallayout_7.setObjectName('horizontallayout_7')
        self.passwords_label = QtWidgets.QLabel(self.passwords_label_frame)
        self.passwords_label.setObjectName('passwords_label')
        self.horizontallayout_7.addWidget(self.passwords_label)
        self.horizontallayout_6.addWidget(self.passwords_label_frame)
        self.verticallayout_3.addWidget(self.labels_frame)
        self.spin_boxes_frame = QtWidgets.QFrame(self.spins_frame)
        self.spin_boxes_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.spin_boxes_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.spin_boxes_frame.setObjectName('spin_boxes_frame')
        self.horizontallayout_5 = QtWidgets.QHBoxLayout(self.spin_boxes_frame)
        self.horizontallayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout_5.setSpacing(0)
        self.horizontallayout_5.setObjectName('horizontallayout_5')
        self.number_of_characters = QtWidgets.QSpinBox(self.spin_boxes_frame)
        self.number_of_characters.setMinimum(1)
        self.number_of_characters.setMaximum(64)
        self.number_of_characters.setObjectName('number_of_characters')
        self.horizontallayout_5.addWidget(self.number_of_characters)
        self.number_of_passwords = QtWidgets.QSpinBox(self.spin_boxes_frame)
        self.number_of_passwords.setMinimum(1)
        self.number_of_passwords.setObjectName('number_of_passwords')
        self.horizontallayout_5.addWidget(self.number_of_passwords)
        self.verticallayout_3.addWidget(self.spin_boxes_frame)
        self.horizontallayout_4.addWidget(self.spins_frame)

        self.characters_label.setText('Number of Imagess')
        self.passwords_label.setText('Post Offset')

        self.auth_button = QtWidgets.QPushButton('Set Auth')
        self.auth_button.setObjectName('number_of_characters')
        self.verticallayout_3.addWidget(self.auth_button)
        
        
            
    

    def open_menu(self):
        if not self.menu_open:
            self.menu_ui()
        else:
            self.close_menu()


    def close_menu(self):
        
        # Hide menu
        self.options_frame.hide()

        # Reset window size
        self.layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        # Reset menu button icon
        self.menu_button.setText('☰')

        # Set menu open flag
        self.menu_open = False        
        

    def open_password_ouput(self):
        if not self.password_output_open:
            self.password_ui()
            self.generate_passwords()
        else:
            self.generate_passwords()



    def close_password_ouput(self):
        self.create_main_ui()


    def password_ui(self):

        # Set open flag
        self.password_output_open = True

        # Change menu button to 'open'
        self.menu_button.setText('☷')

        # Create output frame
        self.output_frame = QtWidgets.QFrame(self.centralWidget)
        self.output_frame.setObjectName('output_frame')
        self.horizontallayout_14 = QtWidgets.QHBoxLayout(self.output_frame)
        self.horizontallayout_14.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontallayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontallayout_14.setSpacing(0)
        self.horizontallayout_14.setObjectName('horizontallayout_14')

        # Add output frame to layout
        self.verticalLayout_10.addWidget(self.output_frame)

        # Create output box
        self.password_output = QtWidgets.QTextEdit(self.output_frame)
        self.password_output.setReadOnly(True)
        self.password_output.setSizePolicy(QtWidgets.QSizePolicy.Preferred, 
                                           QtWidgets.QSizePolicy.Expanding)
        self.password_output.setStyleSheet('font: bold 12px;'
                                           'background: #FFFFFF; '
                                           'border: 1px solid #272727')

        self.horizontallayout_14.addWidget(self.password_output)



    def generate_passwords(self):

        # Increase window size
        #self.resize(500, 50)

        # Clear the output box
        self.password_output.setText('')

        # Set strings to get characters from
        # Numbers
        numbers = string.digits
        # Letters
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        # Special Characters
        special_characters = '!@#$%^&*()\{\}[]?,.'

        # Init output character string
        output_characters = ''

        # Init empty password list
        final_password_list = []

        # Check user has used a lowercase_checkbox, add characters from strings relative to checkboxes, generate password
        if True in [self.numbers_checkbox.isChecked(), 
                    self.lowercase_checkbox.isChecked(), 
                    self.uppercase_checkbox.isChecked(),
                    self.special_characters_checkbox.isChecked()]:

            output_characters = (numbers * self.numbers_checkbox.isChecked() 
                                  + lowercase * self.lowercase_checkbox.isChecked() 
                                  + uppercase * self.uppercase_checkbox.isChecked() 
                                  + special_characters * self.special_characters_checkbox.isChecked())
            # Check how many passwords the user requires, generate for that amount
            for i in range(0, self.number_of_passwords.value()):

                password = ''.join(random.choice(output_characters) for i in range(self.number_of_characters.value()))

                final_password_list.append(password)

        # If user hasn't selected a lowercase_checkbox, inform them in a popup
        else:
            informer = QMessageBox()
            #informer.setWindowTitle('Passwordy - Error')
            informer.setStandardButtons(QMessageBox.Ok)
            informer.setDefaultButton(QMessageBox.Ok)
                # Warning text
            informer.setText('Error: ' + '\n' + 'You must make a selection using one of the checkboxes, please try again...')
            informer.exec_()

        # Add each password in the password list to the output box
        for i in final_password_list:
            self.password_output.append(i)


    def mousePressEvent(self, event):
        self.offset = event.pos()


    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)
    
 
# Run App
def main():
 
    app = QtWidgets.QApplication(sys.argv)
 
    main = Tumbly()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    
    main()
