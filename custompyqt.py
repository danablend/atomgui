from PyQt5.QtCore import pyqtProperty
import PyQt5.QtCore as Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtGui import QPixmap

class QTextedImage(QWidget):
    def __init__(self, text, img, parent=None): # Text = Text (String) / img = Path to image (String)
        QWidget.__init__(self, parent)

        self.parent = parent
        self._text = text
        self._img = img

        self.setLayout(QVBoxLayout())
        self.lbPixmap = QLabel(self)
        self.lbPixmap.setAlignment(Qt.Qt.AlignCenter)
        self.lbText = QLabel(self)
        self.lbText.setAlignment(Qt.Qt.AlignCenter)
        #self.lbText.setTextFormat(Qt.Qt.RichText)

        stylesheet = """
        .QLabel {
            border: 1px solid black;
            font-family: Calibri;
            font-size: 24px;
            }
        """
        self.setStyleSheet(stylesheet)

        self.layout().addWidget(self.lbPixmap)
        self.layout().addWidget(self.lbText)

        self.initUi()

    def initUi(self):
        self.lbPixmap.setPixmap(QPixmap(self._img).scaled(
            self.lbPixmap.size(), Qt.Qt.KeepAspectRatio))
        self.lbText.setText(self._text)

    @pyqtProperty(str)
    def img(self):
        return self._img

    @img.setter
    def total(self, value):
        if self._img == value:
            return
        self._img = value
        self.initUi()

    @pyqtProperty(str)
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return
        self._text = value
        self.initUi()

    def setPixmap(self, value):
        if self.lbPixmap.pixmap == value:
            return
        self.lbPixmap.setPixmap(value)
    
    def getTextLabel(self):
        label = QLabel(self.parent)
        label.text = self.text
        return label
    
    def getImageLabel(self):
        label = QLabel(self.parent)
        label.pixmap = self.lbPixmap.pixmap
        return label