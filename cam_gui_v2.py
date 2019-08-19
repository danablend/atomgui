import sys
import settings

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel, QSplitter, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QTimer, QRect
from custompyqt import QTextedImage
import PyQt5 as Qt
import cv2

class Image(QPixmap):

    def __init__(self, path):
        super.__init__()
        self.cvimg = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.pixmap = QPixmap(self.path).scaled(self.cvimg.width, self.cvimg.height, Qt.QtCore.Qt.KeepAspectRatio, Qt.QtCore.Qt.FastTransformation)

class QuantumGui(QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'Imaging'
        self.left = 5
        self.top = 5
        self.width = 800
        self.height = 500

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setupGui()
        self.show()
        self.update()

        #self.timer = QTimer()
        #self.timer.timeout.connect(self.update) # Means that this timer will be calling the 'self.update()' method
        #self.timer.start(settings.guiUpdateInterval) # Starts the timer and updates it at a given interval

    def setupGui(self):
        self.window = QWidget()
        self.container = QHBoxLayout()

        self.left = QSplitter(Qt.QtCore.Qt.Vertical)
        self.right = QSplitter(Qt.QtCore.Qt.Vertical)

        self.rightwrapper = QSplitter(Qt.QtCore.Qt.Vertical)

        # Adding the images before updating
        img1 = QLabel(self.left)
        pix1 = QPixmap("snap_1,1.tif").scaled(696, 512, Qt.QtCore.Qt.KeepAspectRatio)
        img1.setPixmap(pix1)

        img2 = QLabel(self.rightwrapper)
        pix2 = QPixmap("snap_1,2.tif").scaled(696, 512, Qt.QtCore.Qt.KeepAspectRatio)
        img2.setPixmap(pix2)
        
        img3 = QLabel(self.rightwrapper)
        pix3 = QPixmap("snap_1,3.tif").scaled(696, 512, Qt.QtCore.Qt.KeepAspectRatio)
        img3.setPixmap(pix3)

        img3 = QLabel(self.rightwrapper)
        pix3 = QPixmap("snap_1,3.tif").scaled(
            696, 512, Qt.QtCore.Qt.KeepAspectRatio)
        img3.setPixmap(pix3)

        self.right.addWidget(self.rightwrapper)

        self.container.addWidget(self.left)
        self.container.addWidget(self.right)
        self.window.setLayout(self.container)

        self.setCentralWidget(self.window)
    
    def update(self):
        pass


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = QuantumGui()
	sys.exit(app.exec_())
