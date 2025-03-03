import cv2
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

class ImageDataset(Dataset):
    def __init__(self, imagePaths):
        self.imagePaths = imagePaths
        self.TARGET_HEIGHT = 256
        self.TARGET_WIDTH = 256

    def __len__(self):
        return len(self.imagePaths)

    def __getitem__(self, idx):
        image = cv2.imread(self.imagePaths[idx])
        imageRgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        resizedImage = self.resizeImage(imageRgb)
        float32Image = torch.tensor(resizedImage, dtype=torch.float32)
        imageTensor = float32Image.permute(2, 0, 1) / 255.0 # Normalize
        #finalTensor = imageTensor.unsqueeze(0)
        return imageTensor # [1, 3, 256, 256]
    
    def resizeImage(self, image):
        image = cv2.resize(image, (self.TARGET_WIDTH, self.TARGET_HEIGHT))
        height, width = image.shape[:2]
        
        # Pad image if below the target size
        top = bottom = (self.TARGET_HEIGHT - height) // 2
        left = right = (self.TARGET_WIDTH - width) // 2

        # Apply padding 
        paddedImage = cv2.copyMakeBorder(
            image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )

        return paddedImage