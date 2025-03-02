from .NeuralNetwork import Gan
from .GuiHelper import GuiHelper
from .DataImporter import DataLoad

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)

app = QApplication(sys.argv)

class Gui(QWidget):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle("Image Generator")
        self.setGeometry(100, 100, 320, 210)
        
        self.layout = QVBoxLayout()
        
        # Mapping Buttons
        self.TrainingDataLine()
        self.TestDataLine()
        self.RunButton()
        self.ExitButton()
        
        self.show()
        sys.exit(app.exec())
        
        Gan()
        print("Looking good")
    
    def GuiStateMachine(self):
        pass
    
    def TrainingDataLine(self):
        self.imageBox1 = QLineEdit(
            self,
            placeholderText='Enter File Location of Training Data',
            clearButtonEnabled=True
        )
        
        # settting and adding button
        self.layout.addWidget(self.imageBox1)
        self.setLayout(self.layout)
        
    def TestDataLine(self):
        self.imageBox2 = QLineEdit(
            self,
            placeholderText='Enter File Location of Test Data',
            clearButtonEnabled=True
        )
        
        # settting and adding button
        self.layout.addWidget(self.imageBox2)
        self.setLayout(self.layout)
    
    # Maps run button to Gui
    def RunButton(self):
        # Mapping button to RunProgram() function
        button = QPushButton('Run')
        button.clicked.connect(GuiHelper.RunProgram)
        
        # setting and adding button
        self.setLayout(self.layout)
        self.layout.addWidget(button)
        
    # Maps exit button to Gui
    def ExitButton(self):
        # Mapping button to ExitProgram() function
        button = QPushButton('Exit')
        button.setGeometry(200, 150, 100, 40) 
        button.clicked.connect(GuiHelper.ExitProgram)
        
        # setting and adding button
        self.setLayout(self.layout)
        self.layout.addWidget(button)
        
        
