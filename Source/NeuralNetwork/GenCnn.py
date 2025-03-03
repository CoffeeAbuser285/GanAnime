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
import torch.nn as nn

from torch.optim import Adam
from torch import flatten
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset

class GenCnn(Module):
    def __init__(self, zDim=100, imageChannels=3):
        super(GenCnn, self).__init__()
        
        self.model = nn.Sequential(
            nn.ConvTranspose2d(zDim, 1024, kernel_size=4, stride=1, padding=0),  # 1x1 → 4x4
            nn.BatchNorm2d(1024),
            nn.ReLU(),

            nn.ConvTranspose2d(1024, 512, kernel_size=4, stride=2, padding=1),  # 4x4 → 8x8
            nn.BatchNorm2d(512),
            nn.ReLU(),

            nn.ConvTranspose2d(512, 256, kernel_size=4, stride=2, padding=1),  # 8x8 → 16x16
            nn.BatchNorm2d(256),
            nn.ReLU(),

            nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1),  # 16x16 → 32x32
            nn.BatchNorm2d(128),
            nn.ReLU(),

            nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1),  # 32x32 → 64x64
            nn.BatchNorm2d(64),
            nn.ReLU(),

            nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2, padding=1),  # 64x64 → 128x128
            nn.BatchNorm2d(32),
            nn.ReLU(),

            nn.ConvTranspose2d(32, imageChannels, kernel_size=4, stride=2, padding=1),  # 128x128 → 256x256
            nn.Tanh()  # Output is scaled between [-1,1]
        )

    def forward(self, x):
        return self.model(x)
    