from .NeuralNetwork import Gan
from .GuiHelper import GuiHelper
from .DataImporter import DataLoad

import time
import os
import sys
from pathlib import Path
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

app = QApplication(sys.argv)

class Gui(QWidget, GuiHelper):
    def __init__(self, *args, **kwargs): 
        QWidget.__init__(self, *args, **kwargs)
        
        # Creating Window
        self.setWindowTitle("Image Generator")
        self.setGeometry(100, 100, 320, 210)
        self.layout = QGridLayout()
        
        # Mapping Files
        self.FindTrainingDataFolder()
        self.FindTestDataFolder()
        self.FindResultDataFolder()
        
        # Progress Bar
        self.AddProgressBar()
        
        # Mapping Buttons
        self.RunButton()
        self.ExitButton()
        
        # Setting layout
        self.setLayout(self.layout)
        
        # Displaying Gui
        self.show()
        sys.exit(app.exec())
    
    # File Location for Training Data
    def FindTrainingDataFolder(self):
        # File selection
        self.fileBrowser1.clicked.connect(lambda: self.OpenFileDialog(self.trainingDataFolder, True))
        self.trainingDataFolder = QLineEdit(self)
        
        # Adding Widgets
        self.layout.addWidget(QLabel('Training Data Folder:'), 1, 0)
        self.layout.addWidget(self.trainingDataFolder, 1, 1)
        self.layout.addWidget(self.fileBrowser1, 1, 2)
        
    # File Location for Test Data
    def FindTestDataFolder(self):
        # File selection
        self.fileBrowser2.clicked.connect(lambda: self.OpenFileDialog(self.testDataFolder, True))
        self.testDataFolder = QLineEdit(self)
        
        # Adding Widgets
        self.layout.addWidget(QLabel('Test Data Folder:'), 3, 0)
        self.layout.addWidget(self.testDataFolder, 3, 1)
        self.layout.addWidget(self.fileBrowser2, 3, 2)
        
    # File Location to Save Resulting Data    
    def FindResultDataFolder(self):
        # File selection
        self.fileBrowser3.clicked.connect(lambda: self.OpenFileDialog(self.resultDataFolder))
        self.resultDataFolder = QLineEdit(self)
        
        # Adding Widgets
        self.layout.addWidget(QLabel('Result Data Folder:'), 5, 0)
        self.layout.addWidget(self.resultDataFolder, 5, 1)
        self.layout.addWidget(self.fileBrowser3, 5, 2)
    
    def AddProgressBar(self):
        self.layout.addWidget(self.pbar, 7, 1)
    
    # Maps run button to Gui
    def RunButton(self):
        # Mapping button to RunProgram() function
        self.runButton.clicked.connect(self.RunProgram)
        
        # Setting and adding button
        self.layout.addWidget(self.runButton, 10, 1)
        
    # Maps exit button to Gui
    def ExitButton(self):
        # Mapping button to ExitProgram() function
        self.exitButton.clicked.connect(self.ExitProgram)
        
        # Setting and adding button
        self.layout.addWidget(self.exitButton, 11, 1)
    
    def ExitProgram(self):
        sys.exit()
        
    # TODO: Link up Progess Bar with the status of the neural network
    def ProgressBar(self):
        # setting for loop to set value of progress bar 
        for i in range(101): 
  
            # slowing down the loop 
            time.sleep(0.05) 
  
            # setting value to progress bar 
            self.pbar.setValue(i) 
                
    def LoadData():
        pass
    
    # Run Program
    def RunProgram(self):
        print(self.testDataFolder.text())
        if not self.CheckIfReady():
            return
        
        self.DisableButtons()
        
        # Starting Progress Bar Thread
        self.StartThread(self.ProgressBar, self.EnableButtons)
        
        
    
        
