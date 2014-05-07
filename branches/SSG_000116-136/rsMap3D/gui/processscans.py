'''
 Copyright (c) 2012, UChicago Argonne, LLC
 See LICENSE file.
'''
import os

import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore

from rsMap3D.mappers.gridmapper import QGridMapper
from rsMap3D.mappers.polemapper import PoleFigureMapper
from rsMap3D.gui.qtsignalstrings import CLICKED_SIGNAL, EDIT_FINISHED_SIGNAL

WARNING_STR = "Warning"

class ProcessScans(qtGui.QDialog):
    '''
    This class presents a form to select to start analysis.  This display
    allows switching between Grid map and pole figure.
    '''
    POLE_MAP_STR = "Pole Map"
    GRID_MAP_STR = "Grid Map"
    
    def __init__(self, parent=None):
        '''
        Constructor - Layout widgets on the page & link up actions.
        '''
        super(ProcessScans, self).__init__(parent)
        self.Mapper = None
        layout = qtGui.QVBoxLayout()

        self.dataBox = self._createDataBox()
        controlBox = self._createControlBox()
        

        layout.addWidget(self.dataBox)
        layout.addWidget(controlBox)
        self.setLayout(layout)                    
        
        
        
    def browseForOutputFile(self):
        '''
        Launch file browser to select the output file.  Checks are done to make
        sure the selected directory exists and that the selected file is 
        writable
        '''
        if self.outFileTxt.text() == "":
            fileName = str(qtGui.QFileDialog.getSaveFileName(None, \
                                               "Save File", \
                                               filter="*.vti"))
        else:
            inFileName = str(self.outFileTxt.text())
            fileName = str(qtGui.QFileDialog.getOpenFileName(None, 
                                               "Save File", 
                                               filter="*.vti", \
                                               directory = inFileName))
        if fileName != "":
            if os.path.exists(os.path.dirname(str(fileName))):
                self.outFileTxt.setText(fileName)
                self.outputFileName = fileName
                self.outFileTxt.emit(qtCore.SIGNAL(EDIT_FINISHED_SIGNAL))
            else:
                message = qtGui.QMessageBox()
                message.warning(self, \
                             WARNING_STR, \
                             "The specified directory does not exist")
                self.outFileTxt.setText(fileName)
                self.outputFileName = fileName
                self.outFileTxt.emit(qtCore.SIGNAL(EDIT_FINISHED_SIGNAL))
            if not os.access(os.path.dirname(fileName), os.W_OK):
                message = qtGui.QMessageBox()
                message.warning(self, \
                             WARNING_STR, \
                             "The specified file is not writable")
            
    def cancelProcess(self):
        '''
        Emit a signal to trigger the cancellation of processing.
        '''
        self.emit(qtCore.SIGNAL("cancelProcess"))
        
    def _createControlBox(self):
        controlBox = qtGui.QGroupBox()
        controlLayout = qtGui.QGridLayout()
        row = 0
        self.progressBar = qtGui.QProgressBar()
        controlLayout.addWidget(self.progressBar,row, 1)

        self.runButton = qtGui.QPushButton("Run")
        controlLayout.addWidget(self.runButton, row, 3)

        self.cancelButton = qtGui.QPushButton("Cancel")
        self.cancelButton.setDisabled(True)

        controlLayout.addWidget(self.cancelButton, row, 4)

        self.connect(self.runButton, \
                     qtCore.SIGNAL(CLICKED_SIGNAL), \
                     self.process)
        self.connect(self.cancelButton, \
                     qtCore.SIGNAL(CLICKED_SIGNAL), \
                     self.cancelProcess)
        self.connect(self, \
                     qtCore.SIGNAL("updateProgress"), \
                     self.setProgress)
        controlBox.setLayout(controlLayout)
        return controlBox
        
    def _createDataBox(self):
        '''
        Create Sub Layout for data gathering widgets
        '''
        dataBox = qtGui.QGroupBox()
        dataLayout = qtGui.QGridLayout()
        row = 0       
#        label = QLabel("Output Type")        
#        dataLayout.addWidget(label, row, 0)
        self.outTypeChooser = qtGui.QComboBox()
        self.outTypeChooser.addItem(self.GRID_MAP_STR)
        self.outTypeChooser.addItem(self.POLE_MAP_STR)
#        dataLayout.addWidget(self.outTypeChooser, row,1)
#        row += 1

        label = qtGui.QLabel("Grid Dimensions")
        dataLayout.addWidget(label, row,0)
        row += 1
        label = qtGui.QLabel("X")
        dataLayout.addWidget(label, row,0)
        self.xDimTxt = qtGui.QLineEdit()
        self.xDimTxt.setText("200")
        self.xDimValidator = qtGui.QIntValidator()
        self.xDimTxt.setValidator(self.xDimValidator)
        dataLayout.addWidget(self.xDimTxt, row,1)
        
        row += 1
        label = qtGui.QLabel("Y")
        dataLayout.addWidget(label, row,0)
        self.yDimTxt = qtGui.QLineEdit()
        self.yDimTxt.setText("200")
        self.yDimValidator = qtGui.QIntValidator()
        self.yDimTxt.setValidator(self.yDimValidator)
        dataLayout.addWidget(self.yDimTxt, row,1)
        
        row += 1
        label = qtGui.QLabel("Z")
        dataLayout.addWidget(label, row,0)
        self.zDimTxt = qtGui.QLineEdit()
        self.zDimTxt.setText("200")
        self.zDimValidator = qtGui.QIntValidator()
        self.zDimTxt.setValidator(self.zDimValidator)
        dataLayout.addWidget(self.zDimTxt, row,1)
        
        row += 1
        label = qtGui.QLabel("Output File")
        dataLayout.addWidget(label, row,0)
        self.outputFileName = ""
        self.outFileTxt = qtGui.QLineEdit()
        self.outFileTxt.setText(self.outputFileName)
        dataLayout.addWidget(self.outFileTxt, row,1)
        self.outputFileButton = qtGui.QPushButton("Browse")
        dataLayout.addWidget(self.outputFileButton, row, 2)

        self.connect(self.outputFileButton, \
                     qtCore.SIGNAL(CLICKED_SIGNAL), 
                     self.browseForOutputFile)
        self.connect(self.outputFileButton, \
                     qtCore.SIGNAL(EDIT_FINISHED_SIGNAL), 
                     self.editFinishedOutputFile)
        self.connect(self.outFileTxt, \
                     qtCore.SIGNAL(EDIT_FINISHED_SIGNAL), \
                     self.editFinishedOutputFile)
        self.connect(self, qtCore.SIGNAL("setFileName"), 
                     self.outFileTxt.setText)
        
        dataBox.setLayout(dataLayout)
        return dataBox
        
    def editFinishedOutputFile(self):
        '''
        When edititing is finished the a check is done to make sure that the 
        directory exists and the file is writable
        '''
        fileName = str(self.outFileTxt.text())
        if fileName != "":
            if os.path.exists(os.path.dirname(fileName)):
                #self.outFileTxt.setText(fileName)
                self.outputFileName = fileName
                #self.outFileTxt.emit(qtCore.SIGNAL("editingFinished()"))
            else:
                if os.path.dirname(fileName) == "":
                    print("joining filename with current path")
                    curDir = os.path.realpath(os.path.curdir)
                    fileName = str(os.path.join(curDir, fileName))
                else:
                    message = qtGui.QMessageBox()
                    message.warning(self, \
                                 WARNING_STR, \
                                 "The specified directory \n" + \
                                 str(os.path.dirname(fileName)) + \
                                 "\ndoes not exist")
                
#               self.outputFileName = fileName
                self.emit(qtCore.SIGNAL("setFileName"), fileName)
                
            if not os.access(os.path.dirname(fileName), os.W_OK):
                message = qtGui.QMessageBox()
                message.warning(self, \
                             WARNING_STR, \
                             "The specified fileis not writable")

    def process(self):
        '''
        Emit a signal to trigger the start of procesing.
        '''
        self.emit(qtCore.SIGNAL("process"))
        
    def runMapper(self, dataSource, transform):
        '''
        Run the selected mapper
        '''
        self.dataSource = dataSource
        nx = int(self.xDimTxt.text())
        ny = int(self.yDimTxt.text())
        nz = int(self.zDimTxt.text())
        if self.outputFileName == "":
            self.outputFileName = os.path.join(dataSource.projectDir,  \
                                               "%s.vti" %dataSource.projectName)
            self.emit(qtCore.SIGNAL("setFileName"), self.outputFileName)
        if os.access(os.path.dirname(self.outputFileName), os.W_OK):
            if (self.outTypeChooser.currentText() == self.GRID_MAP_STR):
                self.mapper = QGridMapper(dataSource, \
                                         self.outputFileName, \
                                         nx=nx, ny=ny, nz=nz,
                                         transform = transform)
                self.mapper.setProgressUpdater(self.updateProgress)
                self.mapper.doMap()
            else:
                self.mapper = PoleFigureMapper(dataSource, \
                                              self.outputFileName, \
                                              nx=nx, ny=ny, nz=nz, \
                                              transform = transform)
                self.mapper.doMap()
        else:
            self.emit(qtCore.SIGNAL("processError"), \
                         "The specified directory \n" + \
                         str(os.path.dirname(self.outputFileName)) + \
                         "\nis not writable")

    def setCancelOK(self):
        '''
        If Cancel is OK the run button is disabled and the cancel button is 
        enabled
        '''
        self.runButton.setDisabled(True)
        self.cancelButton.setDisabled(False)
        self.dataBox.setDisabled(True)

    def setOutFileName(self, name):
        '''
        Write a filename to the text widget and to the stored output file name
        '''
        self.outFileTxt.setText(name)
        self.outputFileName = name
        
    def setProgress(self, value):
        '''
        Set the value in the progress bar
        '''
        self.progressBar.setValue(value)
        
    def setProgressLimits(self, min, max):
        '''
        Set the limits on the progress bar.
        '''
        self.progressBar.setMinimum(min)
        self.progressBar.setMaximum(max)
        
    def setRunOK(self):
        '''
        If Run is OK the load button is enabled and the cancel button is 
        disabled
        '''
        self.runButton.setDisabled(False)
        self.cancelButton.setDisabled(True)
        self.dataBox.setDisabled(False)
        
    def stopMapper(self):
        '''
        Halt the mapping process
        '''
        self.mapper.stopMap()
        
    def updateProgress(self, value):
        '''
        Send signal to update the progress bar.
        '''
        self.emit(qtCore.SIGNAL("updateProgress"), value)
        