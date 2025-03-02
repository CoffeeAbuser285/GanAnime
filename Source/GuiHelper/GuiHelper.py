from .ThreadingHelper import ThreadingHelper

import os
import sys
from pathlib import Path
import time

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QListWidget,
    QGridLayout,
    QLabel,
    QProgressBar,
    QMessageBox
)

from PyQt6.QtCore import (
    QThread,
    pyqtSignal
)

IMAGE_EXTENSIONS = {".png", ".jpg"}

class GuiHelper():
    def __init__(self):
        print("GuiHelper")
        
    def LoadData():
        pass
    
    def StartThread(self, func):
        self.thread = ThreadingHelper(func)
        self.thread.finished.connect(lambda: print(str(func), "Thread Finished"))
        self.thread.start()
    
    # File Location for Training Data
    def FindTrainingDataFolder(self):
        # File selection
        FileBrowser = QPushButton('Browse')
        FileBrowser.clicked.connect(lambda: self.OpenFileDialog(self.trainingDataFolder))
        self.trainingDataFolder = QLineEdit(self)
        
        # Adding Widgets
        self.layout.addWidget(QLabel('Training Data Folder:'), 1, 0)
        self.layout.addWidget(self.trainingDataFolder, 1, 1)
        self.layout.addWidget(FileBrowser, 1, 2)
        
    # File Location for Test Data
    def FindTestDataFolder(self):
        # File selection
        FileBrowser = QPushButton('Browse')
        FileBrowser.clicked.connect(lambda: self.OpenFileDialog(self.testDataFolder))
        self.testDataFolder = QLineEdit(self)
        
        # Adding Widgets
        self.layout.addWidget(QLabel('Test Data Folder:'), 3, 0)
        self.layout.addWidget(self.testDataFolder, 3, 1)
        self.layout.addWidget(FileBrowser, 3, 2)
        
    # File Location to Save Resulting Data    
    def FindResultDataFolder(self):
        # File selection
        FileBrowser = QPushButton('Browse')
        FileBrowser.clicked.connect(lambda: self.OpenFileDialog(self.resultDataFolder))
        self.resultDataFolder = QLineEdit(self)
        
        # Adding Widgets
        self.layout.addWidget(QLabel('Result Data Folder:'), 5, 0)
        self.layout.addWidget(self.resultDataFolder, 5, 1)
        self.layout.addWidget(FileBrowser, 5, 2)
    
    def AddProgressBar(self):
        self.layout.addWidget(self.pbar, 7, 1)
    
    # Maps run button to Gui
    def RunButton(self):
        # Mapping button to RunProgram() function
        button = QPushButton('Run')
        button.clicked.connect(self.RunProgram)
        
        # Setting and adding button
        self.layout.addWidget(button,10,1)
        
    # Maps exit button to Gui
    def ExitButton(self):
        # Mapping button to ExitProgram() function
        button = QPushButton('Exit')
        button.clicked.connect(self.ExitProgram)
        
        # Setting and adding button
        self.layout.addWidget(button, 11, 1)
                
    # Open File Dialog
    def OpenFileDialog(self, filePath):
        folderName = QFileDialog.getExistingDirectory(None, "Select a Folder Containing Images")
        
        if folderName:  
            # Check if the folder contains at least one image
            if any(file.lower().endswith(tuple(IMAGE_EXTENSIONS)) for file in os.listdir(folderName)):
                print(f"Selected folder: {folderName}")
                path = Path(folderName)
                filePath.setText(str(path))
            else:
                QMessageBox.warning(None, "Invalid Folder", "The selected folder does not contain any images.")
                
    # Run Program
    def RunProgram(self):
        # Starting Progress Bar Thread
        self.StartThread(self.ProgressBar)
        
    # Progress Bar
    def ProgressBar(self):
        # setting for loop to set value of progress bar 
        for i in range(101): 
  
            # slowing down the loop 
            time.sleep(0.05) 
  
            # setting value to progress bar 
            self.pbar.setValue(i) 
        
    def ExitProgram(self):
        sys.exit()