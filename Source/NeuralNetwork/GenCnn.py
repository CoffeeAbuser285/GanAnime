from torch.nn import Module
from torch.nn import BatchNorm1d
from torch.nn import BatchNorm2d
from torch.nn import Module
from torch.nn import Conv2d
from torch.nn import Linear
from torch.nn import MaxPool2d
from torch.nn import ReLU
from torch.nn import Softmax
from torch.nn import Dropout

from torch.optim import Adam
from torch import flatten
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset

class GenCnn(Module):
    def __init__(self, numChannels, classes):
        super(GenCnn, self).__init__()
        filterSize = (5,5)
        numFilters = 32
        
        self.norm = BatchNorm2d(numChannels)
        self.norm32 = BatchNorm2d(32)
        self.norm64 = BatchNorm2d(64)
        self.norm128 = BatchNorm2d(128)
        self.norm256 = BatchNorm2d(256)
        
        self.norm1d = BatchNorm1d(128)

        self.dropout0p2  = Dropout(p=0.2)
        self.dropout0p3  = Dropout(p=0.3)
        self.dropout0p4  = Dropout(p=0.4)
        self.dropout0p5  = Dropout(p=0.5)
        
        self.relu1 = ReLU()
        self.relu2 = ReLU()
        self.relu3 = ReLU()
        self.relu4 = ReLU()
        self.relu5 = ReLU()

        self.conv10_32 = Conv2d(in_channels=numChannels, out_channels=numFilters, kernel_size=filterSize, padding=2)
        self.conv32_64 = Conv2d(in_channels=32, out_channels=64, kernel_size=filterSize, padding=2)
        self.conv64_128 = Conv2d(in_channels=64, out_channels=128, kernel_size=filterSize, padding=2)
        self.conv128_256 = Conv2d(in_channels=128, out_channels=256, kernel_size=filterSize, padding=2)

        self.maxpool1 = MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        self.maxpool2 = MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        self.maxpool3 = MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        self.maxpool4 = MaxPool2d(kernel_size=(2, 2), stride=(2, 2))

        #final layer
        self.fc1 = Linear(in_features=1024, out_features=128)
        self.fc2 = Linear(in_features=128, out_features=classes)
        self.Softmax = Softmax(dim=1)

    def forward(self, x):
        x = self.norm(x)
        
        #layer1
        x = self.conv10_32(x)
        x = self.relu1(x)
        x = self.norm32(x)
        x = self.maxpool1(x)
        x = self.dropout0p2(x)

        #layer2
        x = self.conv32_64(x)
        x = self.relu2(x)
        x = self.norm64(x)
        x = self.maxpool2(x)
        x = self.dropout0p3(x)
        
        #layer3
        x = self.conv64_128(x)
        x = self.relu3(x)
        x = self.norm128(x)
        x = self.maxpool3(x)
        x = self.dropout0p4(x)
        
        #layer4
        x = self.conv128_256(x)
        x = self.relu4(x)
        x = self.norm256(x)
        x = self.maxpool4(x)
        x = self.dropout0p5(x)
        
        #final layer
        x = flatten(x, 1)
        x = self.fc1(x)
        x = self.relu5(x)
        x = self.norm1d(x)
        x = self.dropout0p5(x)
        x = self.fc2(x)
        x = self.Softmax(x)
        
        return x 
    