from PyQt5.QtWidgets import QApplication
from camera import Lucam
from camera import test
from camera import API
from cam_gui import QuantumGui
import time
import math
import keyboard
import sys
import threading
import settings

class LucamSnapshotUtility:
	
	def __init__(self):
		self.end = False

		self.currentSet = 1

		self.lucam = Lucam()
		# set camera to 16 bit, 4x4 binning, max framerate
		self.lucam.SetFormat(Lucam.FrameFormat(0, 0, 348 * 4, 256 * 4, API.LUCAM_PF_16, binningX=1, flagsX=1, binningY=1, flagsY=1), framerate=100.0)
		# disable all internal image enhancements

		frameformat, framerate = self.lucam.GetFormat()
		pixeldepth = self.lucam.GetTruePixelDepth()
		self.image = self.lucam.TakeSnapshot()

		self.lucam.set_properties(brightness=1.0, contrast=2.0, saturation=1.0, hue=0.0, gamma=1.0, exposure=5.0, gain=2.0)
		snapshot = Lucam.Snapshot(exposure=self.lucam.exposure, gain=1.0, timeout=130.0, format=frameformat)
		self.lucam.EnableFastFrames(snapshot)
		self.lucam.SetTimeout(True, 130.0)	
	
	def snap(self, images):
		for i in range(settings.snapsPerSet):
			img = images[i]
			self.lucam.ForceTakeFastFrame(img, validate=False)
			self.lucam.SaveImage(img, "img/snap_{},{}.tif".format(self.currentSet, i+1))
		# Update gui
		settings.updateGui = True
	
	def startListening(self):
		self.lucam.SetTriggerMode(True)
		print("------ Begin Listening ------")
		self.end = False

		images = list()
		while not self.end:
			try:
				self.lucam.TakeFastFrame(self.image) # If this does not except, camera is triggered
				images.append(self.image)
				if len(images) == settings.snapsPerSet: # Will be true if there are taken snapsPerSet images (Also means 3x camera triggers)
					self.snap(images)
					self.currentSet += 1
					images.clear()
			except:
				pass
		print("------ End Listening ------")
	
	def __del__(self):
		self.lucam.CameraClose()
		del self.lucam
