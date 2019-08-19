import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib
import cv2
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from numpy import exp, loadtxt, pi, sqrt
from lmfit import Model # Update after import to fix import error: pip install --upgrade lmfit
from statistics import mean
import json
import tkinter
from PIL import Image, ImageTk
import itertools
import warnings

# Default images for testing
#try:
    #background = cv2.imread("snap_1,1.png", cv2.IMREAD_GRAYSCALE)
    #laser = cv2.imread("snap_1,2.png", cv2.IMREAD_GRAYSCALE)
    #shadow = cv2.imread("snap_1,3.png", cv2.IMREAD_GRAYSCALE)
    #print(type(shadow))
#except:
    #print("Unable to load default images")

def opticalImageDepth(background, laser, shadow):
    '''
    Optical image depth formula:
    D = image without laser or particles
    L = image with laser only
    S = image with laser and particles
    All represented as arrays/matrix
    ODImage = ln((L - D)/(S - D))
    '''   
    #return background 
    return np.log((laser - background)/(shadow - background))

def adjustValues(y : list) -> list:
    # Adjusts the image to disgard background noise
    y_mean = y - mean(y) # Subtracts the median value from every element in list
    y_min = [min(y_mean)] * len(y) # Creates a list of the lowest value after previous operation
    y_adjusted = y - mean(y) - y_min # Subtracts the median and minimum value. Minimum is a negative int though, so the value actually increases

    return y

def gaussFitData(x: list, y: list) -> (float, float):
    """
    Since it's a gaussian fit for both rows and columns, two seperate 1D gaussian is fitted.
    Reference: https://lmfit.github.io/lmfit-py/model.html
    """

    def gaussian(x, amp, cen, wid, offset):
        """1-d gaussian: gaussian(x, amp, cen, wid)"""
        return (amp / (sqrt(2*pi) * wid)) * exp(-(x-cen)**2 / (2*wid**2)) + offset

    gmodel = Model(gaussian)
    result = gmodel.fit(y, x=x, amp=5, cen=5, wid=1, offset=0)
    #print(result.fit_report())

    # Read the center and width of atom cloud from a json string
    center = result.params["cen"].value
    width = result.params["wid"].value
    amp = result.params["amp"].value
    offset = result.params["offset"].value
    
    return center, width, amp

def cloudAtomCount(xGaussA, xGaussC, yGaussA, yGaussC, ODMAX, delta, gamma, sigmaX, sigmaY, realPixSize, laserWaveLength):
    '''
    Integrating both gauss function from -inf to inf for both the x-axis gauss function, and y-axis gauss function, with the formula:
    int(Gauss function) = a*c*sqrt(2*pi)
    '''
    integralX = xGaussA * xGaussC * sqrt(2*pi) # Integral of x-axis gauss function
    integralY = yGaussA * yGaussC * sqrt(2*pi) # Integral of y-axis gauss function
    integralMean = (integralX + integralY)/2 # Both function should have the same area under the graph, so the mean value is found for precision in case of abnormalities
    
    ODMAX = 1
    gamma = 2.8 # Default number 2.8 Mhz
    delta = 1
    sigma = lambda delta: delta/gamma
    realPixSize = 1

    numberOfAtoms = ((2*pi)**2*ODMAX*(1+sigma(delta)**2)*realPixSize**2*sigmaX*sigmaY)/(3*laserWaveLength**2)

    return numberOfAtoms


def regionOfInterest(img):
    # Sum pixel intensity columns and rows
        # Fit gaurssian function to data points with sci-py. Function for x, and function for y
            # Optimize gaussian fits
    # Crop image to sigma_x and sigma_y  with offset mu_x adn mu_y
    # Integrate gaussian function for number of pixels in cloud
        # Area under both graphs should be the same
    # Multiply number of pixels by constant for number of atoms in the cloud

    # Sums the intensity of each row of pixels
    rows = list()
    for row in img:
        rows.append(sum(row))
    
    # Sums intensity of each column of pixels
    columns = list()
    for i in range(len(img[0])): # Loops through every column
        column = list()
        for j in range(len(img)): # Loops thorugh every row
            column.append(img[j][i])
        columns.append(sum(column))

    # Remove background noise from values, and create a list of x-values
    yRow = adjustValues(rows)
    yColumn = adjustValues(columns)
    xRow = list(range(1, len(yRow) + 1))
    xColumn = list(range(1, len(yColumn) + 1))

    # Calls the gaussian fit function which returns the center and width of atom cloud
    xGaussFit = gaussFitData(xRow, yRow)
    yGaussFit = gaussFitData(xColumn, yColumn)

    xCen, xSigma, xAmp = xGaussFit[0], xGaussFit[1], xGaussFit[2]
    yCen, ySigma, yAmp = yGaussFit[0], yGaussFit[1], yGaussFit[2]

    return img[int(xCen - xSigma*2):int(xCen + xSigma*2), int(yCen - ySigma*2):int(yCen + ySigma*2)], xGaussFit, yGaussFit

def showImage(img, axes):
    #cmap = matplotlib.pyplot.jet()
    #plt.imshow(img, cmap=cmap)
    #plt.colorbar(ticks=[1, 50, 100, 150, 200]) # Tick values is the marks on the colorbar on the plot. Can be customized to whatever
    fig = plt.figure()
    cmapp = plt.jet()
    plt.imshow(img, cmap=cmapp)
    if axes:
        print("Axes is true")
        plt.colorbar(ticks=[1, 50, 100, 150, 200]) # Tick values is the marks on the colorbar on the plot. Can be customized to whatever
    plt.title("Image")
    plt.tight_layout()
    
    #fig, ax = plt.subplots()
    if not axes:
        plt.axis('off')
        #fig.delaxes(ax)
    #plt.show()
    return fig


def xAxisPlot ():
    pass

def yAxisPlot ():
    pass

def imageCvToPil(img):
    # Convert back to rgb to get all three chanels back
    rgbImg = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

    # Convert the Image object into a TkPhoto object
    imgPil = Image.fromarray(rgbImg)
    return (imgPil)

def imagePilToCv(img):
    imgCv = np.array(img)
    # Convert RGB to BGR
    imgCv = imgCv[:, :, ::-1].copy()
    return (imgCv)

"""
plot, xGaussFit, yGaussFit = regionOfInterest(background)
xCenter, xSigma, xAmp, yCenter, ySigma, yAmp = xGaussFit[0], xGaussFit[1], xGaussFit[2], yGaussFit[0], yGaussFit[1], yGaussFit[2]

delta = 4 # Updated automatically
gamma = 2.8 # Constant
realPixelSize = 0.002 # Size of a real pixel
laserWaveLenth = 460 # Entered in GUI
print(opticalImageDepth(background, laser, shadow))
atomCount = cloudAtomCount(xAmp, xSigma, yAmp, ySigma, np.amax(opticalImageDepth(background, laser, shadow)), delta, gamma, xSigma, ySigma, realPixelSize, laserWaveLenth)

#showImage(plot, True, 0)
print("Atom count in cloud:", str(int(atomCount)))
"""