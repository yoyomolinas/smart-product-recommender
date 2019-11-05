import random
import numpy as np
from tensorflow import keras

class TripletGenerator(keras.utils.Sequence):
        def __init__(self, X, Y, batch_size = 64):
            self.batch_size = batch_size
            self.anchor = X[0]
            self.positive = X[1]
            self.negative = X[2]
            self.y = Y
            
        def __len__(self):
            return len(self.y)

        def __getitem__(self, i):
            ret = []
            for i in range(self.batch_size):
                apn = [self.anchor[i],
                       self.positive[i],
                       self.negative[i]]
                ret.append(apn)
            ret = np.array(ret)
            anchor, positive, negative = ret[:, 0], ret[:, 1], ret[:, 2]
            dummy = np.zeros((self.batch_size, 1))
            return [anchor, positive, negative], dummy
