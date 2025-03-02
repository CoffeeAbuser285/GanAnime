import matplotlib.pyplot as plt
import numpy as np
import torch

DATA_FILE = 'data/cifar-10-batches-py/'
TRAIN_FILES = ['data_batch_1', 'data_batch_2','data_batch_3','data_batch_4','data_batch_5']
TEST_FILE   = 'test_batch'

class DataLoad():
    def CnnPrep(self):
        train_data, train_labels, test_data, test_labels = self.file2numpy()
        train_images, test_images                        = self.imageReconstruction(train_data, test_data)
        train_data, test_data                            = self.transposeImage(train_images, test_images)
        train_data, train_labels, test_data, test_labels = self.numpy2torch(train_data, train_labels, test_data, test_labels)
        
        return train_data, train_labels, test_data, test_labels, train_images, test_images
    
    
    def unpickle(self, file):
        import pickle
        with open(file, 'rb') as fo:
            dict = pickle.load(fo, encoding='bytes')
        return dict
    
    
    def file2numpy(self):
        test_dict = self.unpickle(DATA_FILE + TEST_FILE)

        data_key  = list(test_dict.keys())[2] #data key
        label_key = list(test_dict.keys())[1] #label key
        
        test_data = test_dict[data_key]
        test_labels = test_dict[label_key]
        
        train_dict   = self.unpickle(DATA_FILE + TRAIN_FILES[0])
        train_data   = train_dict[data_key]
        train_labels = train_dict[label_key]

        for i in range(1, len(TRAIN_FILES)):
            train_dict   = self.unpickle(DATA_FILE + TRAIN_FILES[i])
            train_data   = np.concatenate((train_data  , train_dict[data_key]))
            train_labels = np.concatenate((train_labels, train_dict[label_key]))
            
        return train_data, train_labels, test_data, test_labels


    def numpy2torch(self, train_data, train_labels, test_data, test_labels):
        train_data   = torch.from_numpy(np.float32(train_data))
        train_labels = torch.from_numpy(np.float32(train_labels))
        test_data    = torch.from_numpy(np.float32(test_data))
        test_labels  = torch.from_numpy(np.float32(test_labels))
        
        return train_data, train_labels, test_data, test_labels
    
    
    def imageReconstruction(self, train_data, test_data):
        x = np.empty([50000,32,32,3],'uint8')
        
        for i in range(len(train_data)):
            red   = train_data[i][0   :1024].reshape(32,32)
            green = train_data[i][1024:2048].reshape(32,32)
            blue  = train_data[i][2048:3072].reshape(32,32)
            x[i] = np.dstack((red, green, blue))
            
        y = np.empty([10000,32,32,3],'uint8')
        
        for i in range(len(test_data)):
            red   = test_data[i][0   :1024].reshape(32,32)
            green = test_data[i][1024:2048].reshape(32,32)
            blue  = test_data[i][2048:3072].reshape(32,32)
            y[i] = np.dstack((red, green, blue))
            
        return x, y
    
    
    def transposeImage(self, train_images, test_images):
        x = np.empty([50000,3,32,32],'uint8')
        
        
        for i in range(len(train_images)):
            x[i] = train_images[i].T
            
        y = np.empty([10000,3,32,32],'uint8')
        
        for i in range(len(test_images)):
            y[i] = test_images[i].T

        return x, y
        