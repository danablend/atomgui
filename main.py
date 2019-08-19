from PyQt5.QtWidgets import (QWidget, QGridLayout,QPushButton, QApplication, QLabel)
from PyQt5.QtGui import QIcon, QPixmap
import PyQt5 as Qt

from cam_gui import QuantumGui
from cam_control import LucamSnapshotUtility

import sys
import threading
import time

util = LucamSnapshotUtility()

def handleCamera():
    global util
    util.startListening()

def handleGui():
    global util

    app = QApplication(sys.argv)

    window = QuantumGui()

    sys.exit(app.exec_())
    
if __name__ == '__main__':
    print("Starting")
    #camThread = threading.Thread(target=handleCamera, args=())
    #camThread.start()
    handleGui()