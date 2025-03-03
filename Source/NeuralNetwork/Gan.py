from .GenCnn import GenCnn
from .GraderCnn import GraderCnn

import time
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader

class Gan():
    def InitializeParameters(self, trainDataLoader, testDataLoader):
        self.INIT_LR = 2e-4
        self.BATCH_SIZE = 32
        self.EPOCHS = 200
        self.W_REG = 0.004
        
        self.lossD = None
        self.lossG = None
        self.randTorch = None
        
        self.trainDataLoader = trainDataLoader
        self.testDataLoader = testDataLoader
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        
        self.GenCnn = GenCnn(100, 3).to(self.device)
        self.GraderCnn = GraderCnn(3).to(self.device)
        
        self.lossBce = nn.BCELoss()
        self.optG = Adam(self.GenCnn.parameters(), lr=self.INIT_LR, betas=(0.5, 0.999))
        self.optD = Adam(self.GraderCnn.parameters(), lr=self.INIT_LR, betas=(0.5, 0.999))
        
    
    def TrainNn(self):
        print("Start Training...")
        
        startTime = time.time()
        
        iteration = []
        accuracy = []
        testAccuracy = []
        
        #training neural network
        for i in range(self.EPOCHS):
            for self.realImages, _ in self.trainDataLoader:
                #y = y.type(torch.LongTensor) 
                #(x,y) = (x.to(self.device), y.to(self.device))
                self.realImages = self.realImages.to(self.device)
                self.batchSize = self.realImages.size(0)
                
                self.realLabels = torch.ones(self.batchSize, 1, device=self.device)
                self.fakeLabels = torch.zeros(self.batchSize, 1, device=self.device)
                
                self.TrainGraderNn()
                self.TrainGeneratorNn()
                
                trainCorrect += sum(outputs.argmax(1) == y)
                
            if i%1 == 0:
                with torch.no_grad():
                    
                    self.cnn.eval()
                    
                    for (x,y) in self.testDataLoader:
                        y = y.type(torch.LongTensor) 
                        (x,y) = (x.to(self.device), y.to(self.device))
                
                        outputs = self.cnn(x)
                        
                        correctCount += sum(outputs.argmax(1) == y)
                        
                print('Test Accuracy: ', round(float(100*correctCount)/len(test_data), 2), '%')
                testAccuracy.append(float(100*correctCount)/len(test_data))
    
    def TrainGraderNn(self):
        # Train Discriminator
        self.randTorch = torch.randn(self.batchSize, 100, 1, 1, device=self.device)
        self.fakeImages = self.GenCnn(self.randTorch)
        realLoss = self.lossBce(self.GraderCnn(self.realImages), self.realLabels)
        fakeLoss = self.lossBce(self.GraderCnn(self.fakeImages.detach()), self.fakeLabels)
        self.lossD = realLoss + fakeLoss
        
        self.optG.zero_grad()
        self.lossG.backward()
        self.optG.step()
                
    def TrainGeneratorNn(self):
        # Train Generator
        self.fakeImages = self.GenCnn(self.randTorch)
        self.lossG = self.lossBce(self.GraderCnn(self.fakeImages), self.realLabels)

        self.optG.zero_grad()
        self.lossG.backward()
        self.optG.step()
        
        self.optD.zero_grad()
        self.lossD.backward()
        self.optD.step()




    
    