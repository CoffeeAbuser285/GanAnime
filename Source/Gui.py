from .NeuralNetwork import Gan
from .GuiHelper import GuiHelper
from .DataImporter import DataLoad

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
        
        # Initializing Variables
        self.trainingDataFolder = ''
        self.testDataFolder = ''
        self.resultDataFolder = ''
        self.pbar = QProgressBar(self)
        
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
    
    # Gui State Machine
    def GuiStateMachine(self):
        pass
    
        
        
