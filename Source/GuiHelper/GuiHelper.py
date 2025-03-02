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
        # Initializing Variables
        self.trainingDataFolder = None
        self.testDataFolder = None
        self.resultDataFolder = None
        
        # Initializing Buttons
        self.pbar = QProgressBar(self)
        self.runButton = QPushButton('Run')
        self.exitButton = QPushButton('Exit')
        self.fileBrowser1 = QPushButton('Browse')
        self.fileBrowser2 = QPushButton('Browse')
        self.fileBrowser3 = QPushButton('Browse')
    
    # Pass in function to run and endFunction
    def StartThread(self, func, endFunc = None):
        self.thread = ThreadingHelper(func)
        self.thread.finished.connect(lambda: print(str(func), "Thread Finished"))
        
        if endFunc != None:
            self.thread.finished.connect(endFunc)
            
        self.thread.start()
    
    def DisableButtons(self):
        self.runButton.setDisabled(True)
        self.fileBrowser1.setDisabled(True)
        self.fileBrowser2.setDisabled(True)
        self.fileBrowser3.setDisabled(True)
        self.trainingDataFolder.setDisabled(True)
        self.testDataFolder.setDisabled(True)
        self.resultDataFolder.setDisabled(True)
        
    def EnableButtons(self):
        self.runButton.setDisabled(False)
        self.fileBrowser1.setDisabled(False)
        self.fileBrowser2.setDisabled(False)
        self.fileBrowser3.setDisabled(False)
        self.trainingDataFolder.setDisabled(False)
        self.testDataFolder.setDisabled(False)
        self.resultDataFolder.setDisabled(False)
        
    # Open File Dialog
    def OpenFileDialog(self, filePath, checkIfImage = False):
        folderName = QFileDialog.getExistingDirectory(None, "Select a Folder Containing Images")
        
        if folderName and checkIfImage:  
            # Check if the folder contains at least one image
            if any(file.lower().endswith(tuple(IMAGE_EXTENSIONS)) for file in os.listdir(folderName)):
                print(f"Selected folder: {folderName}")
                path = Path(folderName)
                filePath.setText(str(path))
            else:
                QMessageBox.warning(None, "Invalid Folder", "The selected folder does not contain any images.")
        elif folderName:
            print(f"Selected folder: {folderName}")
            path = Path(folderName)
            filePath.setText(str(path))
            
    def CheckIfReady(self):
        if not os.path.isdir(self.resultDataFolder.text()):
            QMessageBox.warning(None, "Invalid Folder", "Data Path does not exist.")
            return False
        
        for folderName in [self.trainingDataFolder.text(), self.testDataFolder.text()]: 
            if not os.path.isdir(folderName):
                QMessageBox.warning(None, "Invalid Folder", "Data Path does not exist.")
                return False
            
            if not any(file.lower().endswith(tuple(IMAGE_EXTENSIONS)) for file in os.listdir(folderName)):
                QMessageBox.warning(None, "Invalid Folder", "Training Data or Test Data Folder does not contain any images.")
                return False
        
        return True