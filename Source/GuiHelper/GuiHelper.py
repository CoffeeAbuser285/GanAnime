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
        self.trainingDataFolder = ''
        self.testDataFolder = ''
        self.resultDataFolder = ''
        
        # Initializing Buttons
        self.pbar = QProgressBar(self)
        self.runButton = QPushButton('Run')
        self.exitButton = QPushButton('Exit')
        self.fileBrowser1 = QPushButton('Browse')
        self.fileBrowser2 = QPushButton('Browse')
        self.fileBrowser3 = QPushButton('Browse')
        
    def StartThread(self, func):
        self.thread = ThreadingHelper(func)
        self.thread.finished.connect(lambda: print(str(func), "Thread Finished"))
        self.thread.start()
    
    def DisableButtons(self):
        self.runButton.setDisabled(True)
        self.fileBrowser1.setDisabled(True)
        self.fileBrowser2.setDisabled(True)
        self.fileBrowser3.setDisabled(True)
        self.trainingDataFolder.setDisabled(True)
        self.testDataFolder.setDisabled(True)
        self.resultDataFolder.setDisabled(True)
        
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