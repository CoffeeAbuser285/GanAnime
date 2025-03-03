from .GenCnn import GenCnn
from .GraderCnn import GraderCnn

import time
import torch
from torch import nn
from torch.optim import Adam

class Gan():
    def InitializeParameters(self, trainDataLoader, testDataLoader):
        self.INIT_LR = 1e-3
        self.BATCH_SIZE = 1024
        self.EPOCHS = 200
        self.W_REG = 0.004
        
        self.trainDataLoader = trainDataLoader
        self.testDataLoader = testDataLoader
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.cnn = GenCnn(numChannels = 3, classes = 10).to(self.device)
        self.opt = Adam(self.cnn.parameters(), lr = self.INIT_LR, weight_decay=self.W_REG)
        self.lossFn = nn.NLLLoss()
        
    
    def TrainNn(self):
        print("Start Training...")
        
        startTime = time.time()
        
        iteration = []
        accuracy = []
        testAccuracy = []
        
        #training neural network
        for i in range(self.EPOCHS):
            self.cnn.train()

            trainCorrect = 0
            correctCount = 0
            
            for (x,y) in self.trainDataLoader:
                y = y.type(torch.LongTensor) 
                (x,y) = (x.to(self.device), y.to(self.device))
                outputs = self.cnn(x)
                loss = self.lossFn(outputs, y)
                
                self.opt.zero_grad()
                loss.backward()
                self.opt.step()
                
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
                
    def TrainGenerativeNn(self):
        pass
    
    def TrainGraderNn(self):
        pass



    
    