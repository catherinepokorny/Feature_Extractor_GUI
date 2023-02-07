# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 17:17:28 2023

@author: catpo
"""

import sys, csv, arcpy

from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle, QFileDialog, QDialog, QMessageBox, QSizePolicy, QAction
from PyQt5.QtGui import QStandardItemModel, QStandardItem,  QDoubleValidator, QIntValidator
from PyQt5.QtCore import QVariant
from PyQt5.Qt import Qt

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as WebMapWidget
except:
    from PyQt5.QtWebKitWidgets import QWebView as WebMapWidget

import gui_main 
import core_functions

# =======================================
# GUI event handler and related functions
# =======================================

# query and direct input functions

def selectCountryShapefile():    
    """open file dialog to select input country shapefile"""
    polygonFile, _ = QFileDialog.getOpenFileName(mainWindow,"Select country shapefile", "","Shapefile (*.shp)")
    if polygonFile:
        ui.countryShapefileInput.setText(polygonFile)
    featureExtractionInputs.append(polygonFile)
    mainWindow.statusBar().showMessage('Next, please select the point input shapefile.')
    print(featureExtractionInputs)    

def generateCountriesList():
    fields = arcpy.ListFields(ui.countryShapefileInput.text())
    print(fields)
        
def selectPointShapefile():    
    """open file dialog to select input point data shapefile"""
    pointFile, _ = QFileDialog.getOpenFileName(mainWindow,"Select point shapefile", "","Shapefile (*.shp)")
    if pointFile:
        ui.pointShapefileInput.setText(pointFile)
    featureExtractionInputs.append(pointFile)
    featureExtractionInputs.append(polygonField)
    featureExtractionInputs.append(pointField)
    mainWindow.statusBar().showMessage('Great. Now enter the name of the Central American country you want to extract features for. You MUST hit enter when done typing.')
    print(featureExtractionInputs)    
        
def assignCountryName():
    polygonValue = ui.countryNameLE.text()
    featureExtractionInputs.append(polygonValue)
    mainWindow.statusBar().showMessage('Next up, choose your extraction options. Click Update Extraction Options button when you are done.')
    print(featureExtractionInputs)
    
def assignPointValue():
    comboText = ui.comboBox.currentText()
    if comboText == 'Extract all shops':
        pointValue = ' '
        print(pointValue)
       
    elif comboText == 'Only extract shops of a certain type':
        pointValue = ui.certainShopsComboBox.currentText()
        print(pointValue)
    else:
        print('Error. Please reselect options.')
    featureExtractionInputs.append(pointValue)
    mainWindow.statusBar().showMessage('Now, please set your output shapefile location.')
    print(featureExtractionInputs)    
        
def selectOutputLocation():
    """open file dialog to select output shapefile save location"""
    outputFile, _ = QFileDialog.getSaveFileName(mainWindow,"Select location to write output shapefile", "","Shapefile (*.shp)")
    if outputFile:
        ui.outputShapefileLE.setText(outputFile)
    featureExtractionInputs.append(outputFile)
    mainWindow.statusBar().showMessage('Great, you are set to begin extracting. Hit the Start Feature Extraction button.')
    print(featureExtractionInputs)    

def runExtractor():
    core_functions.FeatureExtraction(*featureExtractionInputs)

#==========================================
# create app and main window + dialog GUI
# =========================================

app = QApplication(sys.argv)

# set up main window

mainWindow = QMainWindow()
ui = gui_main.Ui_MainWindow()
ui.setupUi(mainWindow)

#==========================================
# connect signals
#==========================================
ui.comboBox.addItems(['PLEASE CHOOSE AN OPTION', 'Extract all shops', 'Only extract shops of a certain type'])
ui.certainShopsComboBox.addItems(['PLEASE CHOOSE A SHOP TYPE TO EXTRACT', 'supermarket', 'convenience', 'clothes', 'bakery'])
ui.countryShapefileInputTB.clicked.connect(selectCountryShapefile)
ui.pointShapefileInputTB.clicked.connect(selectPointShapefile)
ui.countryNameLE.returnPressed.connect(assignCountryName)
ui.pushButton.clicked.connect(assignPointValue)
ui.outputShapefileTB.clicked.connect(selectOutputLocation)
ui.startPB.clicked.connect(runExtractor)



#==================================
# initialize global variables
#==================================
# set hardcoded variables

polygonField = 'NAME'
pointField = 'shop'

# create empty list to pass as parameter to FeatureExtraction function

featureExtractionInputs = []




#=======================================
# run app
#=======================================
mainWindow.statusBar().showMessage('First off, please navigate to the country input shapefile.')
mainWindow.show()
sys.exit(app.exec_())