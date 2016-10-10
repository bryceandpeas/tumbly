import os
import sys
import queue

from tumbly.confighandler import put_config
from tumbly.database import create_check_database
from tumbly.scrape import scrape_tumblr
from tumbly.download import download_images

from PyQt5 import QtCore, QtGui, QtWidgets

# Globals
user_username = None
user_number = None
user_offset = None


class WriteStream(object):

    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

    # Everyone loves a no-op
    def flush(self):
        pass


class MyReceiver(QtCore.QObject):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QtCore.QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)


class RunMain(QtCore.QObject):

    @QtCore.pyqtSlot()
    def run(self):

        # Get globals
        global user_username
        global user_number
        global user_offset

        # Init variables
        username = user_username
        url_to_scrape = ''
        database_name = ''
        number = user_number
        offset = user_offset

        # Get user input
        # Create URL
        url_to_scrape = 'http://{0}.tumblr.com'.format(username)
        # Create database name
        database_name = '{0}.db'.format(username)
        # Check if directory exists, create if not
        script_directory = os.path.dirname(os.path.abspath(__file__))
        downloaded_image_directory = os.path.join(script_directory,
                                                  'images',
                                                  '{0}_saved_images'
                                                  .format(username))

        if not os.path.exists(downloaded_image_directory):
            os.makedirs(downloaded_image_directory)

        create_check_database(database_name)

        scrape_tumblr(username,
                      url_to_scrape,
                      database_name,
                      number,
                      offset,
                      limit=20,
                      url_type='blog')

        download_images(username,
                        database_name,
                        downloaded_image_directory,
                        number)

class Tumbly(QtWidgets.QWidget):

    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setObjectName('Tumbly')
        self.resize(500, 500)
        self.setStyleSheet('/* Style tabs */\n'
        '    /* tab_window */\n'
        'QtWidgets.QTabWidget::pane { \n'
        'border-top: 5px solid #21262C;\n'
        '}\n'
        '    /* tabs */\n'
        '/* Style the tab using the tab sub-control. Note that it reads QTabBar _not_ QtWidgets.QTabWidget */\n'
        'QTabBar::tab {\n'
        'background: #21262C;\n'
        'color: #FFB437;\n'
        'border: None;\n'
        'border-bottom-color: #C2C7CB; /* same as the pane color */\n'
        'border-top-left-radius: 4px;\n'
        'border-top-right-radius: 4px;\n'
        'min-width: 8ex;\n'
        'padding: 2px;\n'
        '}\n'
        '\n'
        'QTabBar::tab:selected, QTabBar::tab:hover {\n'
        'background: #FFB437;\n'
        'color: #21262C;\n'
        'border-bottom-color: #21262C;\n'
        'border: None;\n'
        '}\n'
        '\n'
        'QTabBar::tab:selected {\n'
        'border-color: #9B9B9B;\n'
        'border-bottom-color: #C2C7CB; /* same as pane color */\n'
        '}\n'
        'QTabBar::tab:!selected {\n'
        'margin-top: 5px; /* make non-selected tabs look smaller */\n'
        '}\n'
        '/* IMPORTANT: 8< Add the code above here 8< */ QTabBar::tab:selected { /* expand/overlap to the left and right by 4px */ margin-left: -4px; margin-right: -4px; } QTabBar::tab:first:selected { margin-left: 0; /* the first selected tab has nothing to overlap with on the left */ } QTabBar::tab:last:selected { margin-right: 0; /* the last selected tab has nothing to overlap with on the right */ } QTabBar::tab:only-one { margin: 0; /* if there is only one tab, we don\'t want overlapping margins */ }\n'
        '\n'
        '/* Style scrape_tab */\n'
        '\n'
        '#scrape_tab {\n'
        'background: #FFFFFF;\n'
        'color: #FFB437;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#username_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#username_box {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#scrape_settings_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#number_frame {\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#number_label_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#number_label {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#number_input_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#number_input {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#offset_frame {\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#offset_label_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#offset_label {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#offset_input {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#offset_input_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '/* Output box */\n'
        '\n'
        '#output_frame {\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#output_box {\n'
        'background: #FFFFFF;\n'
        'color: #21262C;\n'
        'border: None\n'
        '}\n'
        '\n'
        '/* Progress bar */\n'
        '\n'
        '#progress_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#progress_frame QtWidgets.QProgressBar {\n'
        'border: 2px Solid #21262C;\n'
        'color: #FFB437;\n'
        'qproperty-alignment: AlignCenter;\n'
        'padding: 1px;\n'
        'background: #FFFFFF;\n'
        '}\n'
        '\n'
        '#progress_frame QtWidgets.QProgressBar::chunk {\n'
        'background: #21262C;\n'
        'border-bottom-right-radius: 7px;\n'
        'border-top-right-radius: 7px;\n'
        'border: 1px solid black;\n'
        '}\n'
        '\n'
        '/* Style Data Tab */\n'
        '\n'
        '#data_tab {\n'
        'background: #FFFFFF;\n'
        'color: #FFB437;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#data_output_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#image_label_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#image_label {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#image_out_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#image_out {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#tags_label_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#tags_label {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#tags_out_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#tags_out {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#view_label_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#view_label {\n'
        'qproperty-alignment: AlignCenter;\n'
        'color: #21262C;\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#view_files_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#files_view {\n'
        'color: #21262C;\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '/* Style Settings Tab */\n'
        '\n'
        '#settings_tab {\n'
        'background: #FFFFFF;\n'
        'color: #FFB437;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#top_frame {\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#auth_frame {\n'
        'color: #21262C;\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#auth_label_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#auth_label {\n'
        'border: None;\n'
        'qproperty-alignment: AlignCenter;\n'
        '}\n'
        '\n'
        '#auth_key_frame {\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#auth_key_label_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#auth_key_input_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#auth_key_input {\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#auth_secret_frame {\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#auth_secret_label_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#auth_secret_input_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#auth_secret_input {\n'
        'border: 2px Solid #21262C;\n'
        '}\n'
        '\n'
        '#bottom_frame {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#frame_5 {\n'
        'border: None;\n'
        '}\n'
        '\n'
        '#frame_6 {\n'
        'border: None;\n'
        '}')

        ''' Create GUI '''

        # Set main layout
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName('verticalLayout_2')
        
        # Create tab window
        self.tab_window = QtWidgets.QTabWidget(self)
        self.tab_window.setObjectName('tab_window')

        ''' Scrape tab '''

        # Create scrape tab
        self.scrape_tab = QtWidgets.QWidget()
        self.scrape_tab.setObjectName('scrape_tab')

        # Set scrape tab's layout
        self.scrape_tab_layout = QtWidgets.QVBoxLayout(self.scrape_tab)
        self.scrape_tab_layout.setContentsMargins(11, 11, 11, 11)
        self.scrape_tab_layout.setSpacing(6)
        self.scrape_tab_layout.setObjectName('scrape_tab_layout')

        # Create username frame
        self.username_frame = QtWidgets.QFrame(self.scrape_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_frame.sizePolicy().hasHeightForWidth())
        self.username_frame.setSizePolicy(sizePolicy)
        self.username_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.username_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.username_frame.setObjectName('username_frame')

        # Create username frame's layout
        self.username_frame_layout = QtWidgets.QVBoxLayout(self.username_frame)
        self.username_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.username_frame_layout.setSpacing(6)
        self.username_frame_layout.setObjectName('username_frame_layout')

        # Create username input box
        self.username_box = QtWidgets.QLineEdit(self.username_frame)
        font = QtGui.QFont()
        font.setFamily('Raleway')
        font.setPointSize(18)
        self.username_box.setFont(font)
        self.username_box.setObjectName('username_box')
        self.username_box.textChanged[str].connect(self.text_changed)
        self.username_frame_layout.addWidget(self.username_box)
        self.scrape_tab_layout.addWidget(self.username_frame)
        
        # Create scrape settings frame
        self.scrape_settings_frame = QtWidgets.QFrame(self.scrape_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrape_settings_frame.sizePolicy().hasHeightForWidth())
        self.scrape_settings_frame.setSizePolicy(sizePolicy)
        self.scrape_settings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrape_settings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scrape_settings_frame.setObjectName('scrape_settings_frame')
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrape_settings_frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.number_frame = QtWidgets.QFrame(self.scrape_settings_frame)
        self.number_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.number_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number_frame.setObjectName('number_frame')
        # Create scrape frame's layout
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.number_frame)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName('verticalLayout_4')
        self.number_label_frame = QtWidgets.QFrame(self.number_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_label_frame.sizePolicy().hasHeightForWidth())
        self.number_label_frame.setSizePolicy(sizePolicy)
        self.number_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.number_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number_label_frame.setObjectName('number_label_frame')
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.number_label_frame)
        self.verticalLayout_9.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName('verticalLayout_9')
        self.number_label = QtWidgets.QLabel(self.number_label_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.number_label.sizePolicy().hasHeightForWidth())
        self.number_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily('Raleway')
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.number_label.setFont(font)
        self.number_label.setObjectName('number_label')
        self.verticalLayout_9.addWidget(self.number_label)
        self.verticalLayout_4.addWidget(self.number_label_frame)
        self.number_input_frame = QtWidgets.QFrame(self.number_frame)
        self.number_input_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.number_input_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.number_input_frame.setObjectName('number_input_frame')
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.number_input_frame)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.number_input = QtWidgets.QSpinBox(self.number_input_frame)
        self.number_input.setObjectName('number_input')
        self.number_input.valueChanged[int].connect(self.number_changed)
        self.horizontalLayout_4.addWidget(self.number_input)
        self.verticalLayout_4.addWidget(self.number_input_frame)
        self.horizontalLayout.addWidget(self.number_frame)
        self.offset_frame = QtWidgets.QFrame(self.scrape_settings_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.offset_frame.sizePolicy().hasHeightForWidth())
        self.offset_frame.setSizePolicy(sizePolicy)
        self.offset_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.offset_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.offset_frame.setObjectName('offset_frame')
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.offset_frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName('verticalLayout_3')
        self.offset_label_frame = QtWidgets.QFrame(self.offset_frame)
        self.offset_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.offset_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.offset_label_frame.setObjectName('offset_label_frame')
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.offset_label_frame)
        self.verticalLayout_8.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName('verticalLayout_8')
        self.offset_label = QtWidgets.QLabel(self.offset_label_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.offset_label.sizePolicy().hasHeightForWidth())
        self.offset_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily('Raleway')
        font.setPointSize(18)
        self.offset_label.setFont(font)
        self.offset_label.setObjectName('offset_label')
        self.verticalLayout_8.addWidget(self.offset_label)
        self.verticalLayout_3.addWidget(self.offset_label_frame)
        self.offset_input_frame = QtWidgets.QFrame(self.offset_frame)
        self.offset_input_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.offset_input_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.offset_input_frame.setObjectName('offset_input_frame')
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.offset_input_frame)
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')
        self.offset_input = QtWidgets.QSpinBox(self.offset_input_frame)
        self.offset_input.setMinimum(20)
        self.offset_input.setObjectName('offset_input')
        self.offset_input.valueChanged[int].connect(self.number_changed)

        # Add invisible pushbutton to catch Enter (Return) key
        self.enter = QtWidgets.QPushButton(self)
        self.enter.resize(0,0)
        self.enter.clicked.connect(self.start_thread)
        self.enter.setShortcut('Return')

        # Create output frame
        self.horizontalLayout_5.addWidget(self.offset_input)
        self.verticalLayout_3.addWidget(self.offset_input_frame)
        self.horizontalLayout.addWidget(self.offset_frame)
        self.scrape_tab_layout.addWidget(self.scrape_settings_frame)
        self.output_frame = QtWidgets.QFrame(self.scrape_tab)
        self.output_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.output_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.output_frame.setObjectName('output_frame')
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.output_frame)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName('verticalLayout_6')
        self.output_box = QtWidgets.QTextEdit(self.output_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_box.sizePolicy().hasHeightForWidth())
        self.output_box.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily('Raleway')
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.output_box.setFont(font)
        self.output_box.setObjectName('output_box')
        self.verticalLayout_6.addWidget(self.output_box)
        self.scrape_tab_layout.addWidget(self.output_frame)
        self.progress_frame = QtWidgets.QFrame(self.scrape_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_frame.sizePolicy().hasHeightForWidth())
        self.progress_frame.setSizePolicy(sizePolicy)
        self.progress_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.progress_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.progress_frame.setObjectName('progress_frame')
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.progress_frame)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName('verticalLayout_7')
        self.progress_bar = QtWidgets.QProgressBar(self.progress_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress_bar.sizePolicy().hasHeightForWidth())
        self.progress_bar.setSizePolicy(sizePolicy)
        self.progress_bar.setProperty('value', 24)
        self.progress_bar.setObjectName('progress_bar')
        self.verticalLayout_7.addWidget(self.progress_bar)
        self.scrape_tab_layout.addWidget(self.progress_frame)
        self.tab_window.addTab(self.scrape_tab, '')

        ''' Data tab '''

        self.data_tab = QtWidgets.QWidget()
        self.data_tab.setObjectName('data_tab')
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.data_tab)
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName('horizontalLayout_6')
        self.data_output_frame = QtWidgets.QFrame(self.data_tab)
        self.data_output_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data_output_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data_output_frame.setObjectName('data_output_frame')
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.data_output_frame)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(6)
        self.verticalLayout_11.setObjectName('verticalLayout_11')
        self.image_out_frame = QtWidgets.QFrame(self.data_output_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_out_frame.sizePolicy().hasHeightForWidth())
        self.image_out_frame.setSizePolicy(sizePolicy)
        self.image_out_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.image_out_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.image_out_frame.setObjectName('image_out_frame')
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.image_out_frame)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(6)
        self.verticalLayout_12.setObjectName('verticalLayout_12')
        self.image_label_frame = QtWidgets.QFrame(self.image_out_frame)
        self.image_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.image_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.image_label_frame.setObjectName('image_label_frame')
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.image_label_frame)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setSpacing(6)
        self.verticalLayout_17.setObjectName('verticalLayout_17')
        self.image_label = QtWidgets.QLabel(self.image_label_frame)
        self.image_label.setObjectName('image_label')
        self.verticalLayout_17.addWidget(self.image_label)
        self.verticalLayout_12.addWidget(self.image_label_frame)
        self.image_out = QtWidgets.QGraphicsView(self.image_out_frame)
        self.image_out.setObjectName('image_out')
        self.verticalLayout_12.addWidget(self.image_out)
        self.verticalLayout_11.addWidget(self.image_out_frame)
        self.tags_label_frame = QtWidgets.QFrame(self.data_output_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tags_label_frame.sizePolicy().hasHeightForWidth())
        self.tags_label_frame.setSizePolicy(sizePolicy)
        self.tags_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tags_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tags_label_frame.setObjectName('tags_label_frame')
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.tags_label_frame)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(6)
        self.verticalLayout_16.setObjectName('verticalLayout_16')
        self.tags_label = QtWidgets.QLabel(self.tags_label_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tags_label.sizePolicy().hasHeightForWidth())
        self.tags_label.setSizePolicy(sizePolicy)
        self.tags_label.setObjectName('tags_label')
        self.verticalLayout_16.addWidget(self.tags_label)
        self.verticalLayout_11.addWidget(self.tags_label_frame)
        self.tags_out_frame = QtWidgets.QFrame(self.data_output_frame)
        self.tags_out_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tags_out_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tags_out_frame.setObjectName('tags_out_frame')
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.tags_out_frame)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setSpacing(6)
        self.verticalLayout_13.setObjectName('verticalLayout_13')
        self.tags_out = QtWidgets.QLineEdit(self.tags_out_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tags_out.sizePolicy().hasHeightForWidth())
        self.tags_out.setSizePolicy(sizePolicy)
        self.tags_out.setObjectName('tags_out')
        self.verticalLayout_13.addWidget(self.tags_out)
        self.verticalLayout_11.addWidget(self.tags_out_frame)
        self.horizontalLayout_6.addWidget(self.data_output_frame)
        self.view_files_frame = QtWidgets.QFrame(self.data_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_files_frame.sizePolicy().hasHeightForWidth())
        self.view_files_frame.setSizePolicy(sizePolicy)
        self.view_files_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.view_files_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.view_files_frame.setObjectName('view_files_frame')
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.view_files_frame)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(6)
        self.verticalLayout_18.setObjectName('verticalLayout_18')
        self.view_label_frame = QtWidgets.QFrame(self.view_files_frame)
        self.view_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.view_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.view_label_frame.setObjectName('view_label_frame')
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.view_label_frame)
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_19.setSpacing(6)
        self.verticalLayout_19.setObjectName('verticalLayout_19')
        self.view_label = QtWidgets.QLabel(self.view_label_frame)
        self.view_label.setObjectName('view_label')
        self.verticalLayout_19.addWidget(self.view_label)
        self.verticalLayout_18.addWidget(self.view_label_frame)
        self.files_view = QtWidgets.QTreeView(self.view_files_frame)
        self.files_view.setObjectName('files_view')
        self.verticalLayout_18.addWidget(self.files_view)
        self.horizontalLayout_6.addWidget(self.view_files_frame)
        self.tab_window.addTab(self.data_tab, '')

        ''' Settings tab '''

        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setObjectName('settings_tab')
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.settings_tab)
        self.verticalLayout_10.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName('verticalLayout_10')
        self.top_frame = QtWidgets.QFrame(self.settings_tab)
        self.top_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_frame.setObjectName('top_frame')
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.top_frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName('horizontalLayout_3')
        self.auth_frame = QtWidgets.QFrame(self.top_frame)
        self.auth_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.auth_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.auth_frame.setObjectName('auth_frame')
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.auth_frame)
        self.verticalLayout_14.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_14.setSpacing(6)
        self.verticalLayout_14.setObjectName('verticalLayout_14')
        self.auth_label_frame = QtWidgets.QFrame(self.auth_frame)
        self.auth_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.auth_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.auth_label_frame.setObjectName('auth_label_frame')
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.auth_label_frame)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setSpacing(6)
        self.verticalLayout_15.setObjectName('verticalLayout_15')
        self.auth_label = QtWidgets.QLabel(self.auth_label_frame)
        font = QtGui.QFont()
        font.setFamily('Raleway')
        font.setPointSize(18)
        self.auth_label.setFont(font)
        self.auth_label.setObjectName('auth_label')
        self.verticalLayout_15.addWidget(self.auth_label)
        self.verticalLayout_14.addWidget(self.auth_label_frame)
        self.auth_key_frame = QtWidgets.QFrame(self.auth_frame)
        self.auth_key_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.auth_key_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.auth_key_frame.setObjectName('auth_key_frame')
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.auth_key_frame)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName('horizontalLayout_9')
        self.auth_key_label_frame = QtWidgets.QFrame(self.auth_key_frame)
        self.auth_key_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.auth_key_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.auth_key_label_frame.setObjectName('auth_key_label_frame')
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.auth_key_label_frame)
        self.horizontalLayout_11.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_11.setSpacing(6)
        self.horizontalLayout_11.setObjectName('horizontalLayout_11')
        self.auth_key_label = QtWidgets.QLabel(self.auth_key_label_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auth_key_label.sizePolicy().hasHeightForWidth())
        self.auth_key_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily('Raleway')
        font.setPointSize(18)
        self.auth_key_label.setFont(font)
        self.auth_key_label.setObjectName('auth_key_label')
        self.horizontalLayout_11.addWidget(self.auth_key_label)
        self.horizontalLayout_9.addWidget(self.auth_key_label_frame)
        self.auth_key_input_frame = QtWidgets.QFrame(self.auth_key_frame)
        self.auth_key_input_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.auth_key_input_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.auth_key_input_frame.setObjectName('auth_key_input_frame')
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.auth_key_input_frame)
        self.horizontalLayout_13.setContentsMargins(22, 0, 11, 0)
        self.horizontalLayout_13.setSpacing(6)
        self.horizontalLayout_13.setObjectName('horizontalLayout_13')
        self.auth_key_input = QtWidgets.QLineEdit(self.auth_key_input_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auth_key_input.sizePolicy().hasHeightForWidth())
        self.auth_key_input.setSizePolicy(sizePolicy)
        self.auth_key_input.setObjectName('auth_key_input')
        self.horizontalLayout_13.addWidget(self.auth_key_input)
        self.horizontalLayout_9.addWidget(self.auth_key_input_frame)
        self.verticalLayout_14.addWidget(self.auth_key_frame)
        self.auth_secret_frame = QtWidgets.QFrame(self.auth_frame)
        self.auth_secret_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.auth_secret_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.auth_secret_frame.setObjectName('auth_secret_frame')
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.auth_secret_frame)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName('horizontalLayout_8')
        self.auth_secret_label_frame = QtWidgets.QFrame(self.auth_secret_frame)
        self.auth_secret_label_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.auth_secret_label_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.auth_secret_label_frame.setObjectName('auth_secret_label_frame')
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.auth_secret_label_frame)
        self.horizontalLayout_10.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName('horizontalLayout_10')
        self.auth_secret_label = QtWidgets.QLabel(self.auth_secret_label_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auth_secret_label.sizePolicy().hasHeightForWidth())
        self.auth_secret_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily('Raleway')
        font.setPointSize(18)
        self.auth_secret_label.setFont(font)
        self.auth_secret_label.setObjectName('auth_secret_label')
        self.horizontalLayout_10.addWidget(self.auth_secret_label)
        self.horizontalLayout_8.addWidget(self.auth_secret_label_frame)
        self.auth_secret_input_frame = QtWidgets.QFrame(self.auth_secret_frame)
        self.auth_secret_input_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.auth_secret_input_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.auth_secret_input_frame.setObjectName('auth_secret_input_frame')
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.auth_secret_input_frame)
        self.horizontalLayout_12.setContentsMargins(0, 0, 12, 0)
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName('horizontalLayout_12')
        self.auth_secret_input = QtWidgets.QLineEdit(self.auth_secret_input_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auth_secret_input.sizePolicy().hasHeightForWidth())
        self.auth_secret_input.setSizePolicy(sizePolicy)
        self.auth_secret_input.setObjectName('auth_secret_input')
        self.horizontalLayout_12.addWidget(self.auth_secret_input)
        self.horizontalLayout_8.addWidget(self.auth_secret_input_frame)
        self.verticalLayout_14.addWidget(self.auth_secret_frame)
        self.horizontalLayout_3.addWidget(self.auth_frame)
        self.verticalLayout_10.addWidget(self.top_frame)
        self.bottom_frame = QtWidgets.QFrame(self.settings_tab)
        self.bottom_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom_frame.setObjectName('bottom_frame')
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.bottom_frame)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.frame_5 = QtWidgets.QFrame(self.bottom_frame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName('frame_5')
        self.horizontalLayout_2.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(self.bottom_frame)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName('frame_6')
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.verticalLayout_10.addWidget(self.bottom_frame)
        self.tab_window.addTab(self.settings_tab, '')
        self.verticalLayout_2.addWidget(self.tab_window)

        self.retranslateUi(self)
        self.tab_window.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self, Tumbly):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate('Tumbly', 'Tumbly'))
        self.username_box.setText(_translate('Tumbly', 'Enter username to scrape here'))
        self.number_label.setText(_translate('Tumbly', 'Number of Images'))
        self.offset_label.setText(_translate('Tumbly', 'Post Offset'))
        self.tab_window.setTabText(self.tab_window.indexOf(self.scrape_tab), _translate('Tumbly', 'Scrape'))
        self.image_label.setText(_translate('Tumbly', 'Image'))
        self.tags_label.setText(_translate('Tumbly', 'Tags'))
        self.view_label.setText(_translate('Tumbly', 'File explorer'))
        self.tab_window.setTabText(self.tab_window.indexOf(self.data_tab), _translate('Tumbly', 'Data'))
        self.auth_label.setText(_translate('Tumbly', 'Authorisation'))
        self.auth_key_label.setText(_translate('Tumbly', 'Key'))
        self.auth_secret_label.setText(_translate('Tumbly', 'Secret'))
        self.tab_window.setTabText(self.tab_window.indexOf(self.settings_tab), _translate('Tumbly', 'Settings'))

    ''' Get user input '''

    def text_changed(self, text):
        # Get text changes
        self.username = str(text)
        global user_username
        user_username = self.username

    def number_changed(self, number):
        # Get number changes
        self.number = int(number)
        global user_number
        user_number = self.number

    def offset_changed(self, number):
        # Get offset changes
        self.offset = int(number)
        global user_offset
        user_offset = self.offset

    def add_auth(self):

        key, ok = QtWidgets.QInputDialog.getText(self, 'No config file',
                                             'Enter your app key:')

        if ok:
            app_key = key

        else:
            app_key = ''

        secret, ok = QtWidgets.QInputDialog.getText(self, 'No config file',
                                                'Enter your app secret:')
        if ok:
            app_secret = secret

        else:
            app_secret = ''

        if app_key == '' or app_secret == '':
            input_check = QtWidgets.QMessageBox.question(self,
                                               'Error',
                                               'You must enter an app key'
                                               ' and an app secret to use'
                                               ' tumbly.',
                                               QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Cancel)

            if input_check == QtWidgets.QMessageBox.Retry:
                self.add_auth()

        put_config('config/tumblyconfig.ini',
                   app_key, app_secret)

    ''' Stream console output to output box'''

    @QtCore.pyqtSlot(str)
    def append_text(self, text):
        self.output_box.moveCursor(QtGui.QTextCursor.End)
        self.output_box.insertPlainText(text)

    ''' Run scrape functions in thread '''

    @QtCore.pyqtSlot()
    def start_thread(self):
        # Check config file exists, make one if not
        if not os.path.isfile('config/tumblyconfig.ini'):
            self.add_auth()
        else:
            self.thread = QtCore.QThread()
            self.main_thread = RunMain()
            self.main_thread.moveToThread(self.thread)
            self.thread.started.connect(self.main_thread.run)
            self.thread.start()

''' Main '''

queue = queue.Queue()
sys.stdout = WriteStream(queue)

qapp = QtWidgets.QApplication(sys.argv)
app = Tumbly()
app.show()


thread = QtCore.QThread()
my_receiver = MyReceiver(queue)
my_receiver.mysignal.connect(app.append_text)
my_receiver.moveToThread(thread)
thread.started.connect(my_receiver.run)
thread.start()

qapp.exec_()

