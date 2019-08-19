import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel, QSplitter, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QTimer, QRect
from custompyqt import QTextedImage
import PyQt5 as Qt
import time
import settings
import cv2
from camera_math import imageCvToPil, imagePilToCv, showImage, opticalImageDepth, plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

class Image():

	def __init__(self, path, width, height):
		self.path = path
		self.width = int(width)
		self.height = int(height)
		self.cvimg = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
	
	def getPixmap(self):
		return QPixmap(self.path).scaled(self.width, self.height, Qt.QtCore.Qt.KeepAspectRatio, Qt.QtCore.Qt.FastTransformation)


class QuantumGui(QMainWindow):
	
	def __init__(self):
		super().__init__()

		# The current loaded set
		self.currentSet = 1
		
		#self.background = cv2.imread("test2.png", cv2.IMREAD_GRAYSCALE) # FOR TESTING

		self.title = 'Imaging'
		self.left = 5
		self.top = 5
		self.width = 800
		self.height = 500

		self.images = list() # [0, 1, 2, 3] // [0] = Big image - [1] to [3] = Smaller images
		self.imageLabels = list() # [0, 1, 2, 3] // [0] = Big image - [1] to [3] = Smaller images ---- These are PyQt5 Labels that gets updated.

		# Initializing the UI, loading images and rendering the objects
		self.initUI()

		# QTimer used for updating the images with a given time interval
		self.timer = QTimer()
		self.timer.timeout.connect(self.update) # Means that this timer will be calling the 'self.update()' method
		self.timer.start(settings.guiUpdateInterval) # Starts the timer and updates it at a given interval
    
	def initUI(self):
		# Assigning the title of the window
		self.setWindowTitle(self.title)

		# Assigning dimensions of this object
		self.setGeometry(self.left, self.top, self.width, self.height)

		# Basically initializing all image loading as well as rendering it
		self.createGridLayout(self.currentSet)

		self.show()

	"""
	This function loads the set of images specified, and renders them to the screen (It's only to be used when initiating the class)
	"""
	def createGridLayout(self, set):
		# Load the given set
		self.loadSet(set)

		# The grid
		self.hbox = QHBoxLayout()

		# Object that contains all the stuff to be displayed
		self.central_widget = QWidget()
		self.central_widget.setLayout(self.hbox)
		self.setCentralWidget(self.central_widget)
		
		# Left side = Big Image
		self.left = QSplitter(Qt.QtCore.Qt.Vertical)

		# Right side = 3 Small images
		self.right = QSplitter(Qt.QtCore.Qt.Vertical)

		# Puts the images onto the proper splitters
		for i in range(len(self.imageLabels)):
			label = self.imageLabels[i]
			if i == 3: # Big image is on index 3 in the images list
				print("Adding left side: ",label)
				self.left.addWidget(label)
				self.addToolBar(Qt.QtCore.Qt.BottomToolBarArea,NavigationToolbar(label, self))
			else: # The smaller images are on index 0 through 2 in the images list
				print("Adding right side: ",label)
				self.right.addWidget(label)

		# Splitter is horizontal, first adding left side, then the right side
		self.splitter = QSplitter(Qt.QtCore.Qt.Horizontal)
		self.splitter.addWidget(self.left)
		self.splitter.addWidget(self.right)
		
		self.container = QSplitter(Qt.QtCore.Qt.Vertical)
		self.container.addWidget(self.splitter)

		# Adding the splitter, containg left and right sides, to the main container
		self.hbox.addWidget(self.container)

	"""
	This function loads the set of images specified and updates the image and image labels
	"""
	def loadSet(self, set):
		# Clear the old data
		self.images.clear()
		self.imageLabels.clear()

		# Dimensions of the window
		width = self.geometry().width()
		height = self.geometry().height()

		for i in range(settings.snapsPerSet):
			# Path to the image
			path = "img/snap_{},{}.tiff".format(self.currentSet, i+1)
			
			# Inserting the image object into the image list
			self.images.append(Image(path, int(width/3), int(height / 3 - 105)))
			print(path,":",self.images[i-1].cvimg)

			# Inserting the image (With text) into the list for image labels
			figure = showImage(self.images[i].cvimg, False)
			label = FigureCanvas(figure)

			self.imageLabels.append(label)
		
		label = FigureCanvas(showImage(opticalImageDepth(self.images[0].cvimg, self.images[1].cvimg, self.images[2].cvimg), True))
		self.imageLabels.append(label)
	
	def update(self):
		if not settings.updateGui:
			return
		width = self.geometry().width()
		height = self.geometry().height()
		print(width,height)

		print("Updated")
		self.loadSet(self.currentSet)

		# Hide the old images (Because that's just how PyQt5 works)
		for c in self.left.children():
			c.hide()
		for c in self.right.children():
			c.hide()

		# Loop through newly loaded images, and insert them above the hidden old images
		for i in range(len(self.imageLabels)):
			label = self.imageLabels[i]
			if i == 3:
				#label.setPixmap(self.images[i].getPixmap().scaledToHeight(height - 105)) # Should be relative to the window size
				self.left.insertWidget(i, label)
			else:
				#label.setPixmap(self.images[i].getPixmap().scaledToHeight(height / 3 - 105))  # Should be relative to the window size
				self.right.insertWidget(i-1, label)

		# Update the containers
		self.left.update()
		self.right.update()
		self.splitter.update()
		self.container.update()
		self.hbox.update()
		settings.updateGui = False
		self.currentSet += 1

# Takes an image object from the cv2 framework (Numpy array) and returns the pixmap matching the PyQt5 framework
def cvToQt(im):
	im = imageCvToPil(im)
	im = im.convert("RGBA")
	data = im.tobytes("raw","RGBA")
	qimg = QImage(data, im.size[0], im.size[1], QImage.Format_RGBA8888)
	pixmap = QPixmap(qimg)
	return pixmap

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = QuantumGui()
	sys.exit(app.exec_())
