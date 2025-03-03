from .GenCnn import GenCnn
from .GraderCnn import GraderCnn

import time
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.utils.data import Dataset, DataLoader
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt


class Gan():
    def InitializeParameters(self, trainDataLoader, testDataLoader):
        self.INIT_LR = 2e-4
        self.BATCH_SIZE = 32
        self.EPOCHS = 1
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
        print("Using ", self.device, "for training")
        print("Start Training...")
        
        startTime = time.time()
        
        #training neural network
        for i in range(self.EPOCHS):
            for self.realImages in self.trainDataLoader:
                self.realImages = self.realImages.to(self.device)
                self.batchSize = self.realImages.size(0)
                
                self.realLabels = torch.ones(self.batchSize, 1, 1, 1, device=self.device)
                self.fakeLabels = torch.zeros(self.batchSize, 1, 1, 1, device=self.device)
                
                self.TrainGraderNn()
                self.TrainGeneratorNn()
            
            print(f"Epoch [{self.EPOCHS+1}/{self.EPOCHS}] | D Loss: {self.lossD.item():.4f} | G Loss: {self.lossG.item():.4f}")

            # Save a sample of generated images
            if (self.EPOCHS + 1) % 1 == 0:
                plt.figure(figsize=(5,5))
                with torch.no_grad():
                    sampleImages = GenCnn(torch.randn(16, 100, 1, 1, device=self.device)).cpu()
                sampleImages = (sampleImages + 1) / 2  # Rescale to [0,1]
                grid = torchvision.utils.make_grid(sampleImages, nrow=4)
                plt.imshow(grid.permute(1, 2, 0))
                plt.show()
        
        totalTime = time.time()-startTime
    
        print('Total Training Time: ', round(totalTime, 2), ' seconds\n')
                
            
    def TrainGraderNn(self):
        # Train Discriminator
        self.randTorch = torch.randn(self.batchSize, 100, 1, 1, device=self.device)
        self.fakeImages = self.GenCnn(self.randTorch)
        realLoss = self.lossBce(self.GraderCnn(self.realImages), self.realLabels)
        fakeLoss = self.lossBce(self.GraderCnn(self.fakeImages.detach()), self.fakeLabels)
        self.lossD = realLoss + fakeLoss
        
        self.optG.zero_grad()
        self.lossD.backward()
        self.optG.step()
                
    def TrainGeneratorNn(self):
        # Train Generator
        self.fakeImages = self.GenCnn(self.randTorch)
        self.lossG = self.lossBce(self.GraderCnn(self.fakeImages), self.realLabels)

        self.optG.zero_grad()
        self.lossG.backward()
        self.optG.step()




    
    