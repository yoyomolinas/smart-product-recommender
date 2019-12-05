import random
import numpy as np
from itertools import permutations
from tensorflow import keras
import time
from PIL import Image

class TripletGenerator(keras.utils.Sequence):
        def __init__(self, X, Y, ap_pairs= 10, an_pairs = 10, batch_size = 64, shuffle = True, renew = False, images_as_path = False, image_size = None):
            self.batch_size = batch_size
            self.shuffle = shuffle
            self.renew = renew
            self.images_as_path = images_as_path
            self.image_size = image_size
            self.ap_pairs = ap_pairs
            self.an_pairs = an_pairs
            # self.anchor = X[0]
            # self.positive = X[1]
            # self.negative = X[2]
            self.images = X
            self.labels = Y
            self.unique_labels = np.unique(self.labels)
            self.triplet_index = self.__generate_triplet_index()
            np.random.shuffle(self.triplet_index)

        def __generate_triplet_index(self):
            triplet_index = [] # (anchor_id, positive_id, negative_id) 
            for class_id in self.unique_labels:
                same_class_idx = list(np.where((self.labels == class_id))[0])
                diff_class_idx = list(np.where(self.labels != class_id)[0])
                same_class_perms = list(permutations(same_class_idx,2))
                ap_idx = np.array(random.sample(same_class_perms, k=min(self.ap_pairs, len(same_class_perms)))) #Generating Anchor-Positive pairs
                if len(ap_idx) < 2:
                    continue
                anchor_idx = ap_idx[:, 0]
                pos_idx = ap_idx[:, 1]
                neg_idx = np.array(random.sample(diff_class_idx, k=self.an_pairs))
                assert len(anchor_idx) == len(pos_idx)
                ap_len = min(self.ap_pairs, len(same_class_perms))
                neg_len = self.an_pairs
                for j in range(ap_len):
                    aid, pid = anchor_idx[j], pos_idx[j]
                    for k in range(neg_len):
                        nid = neg_idx[k]
                        triplet_index.append([aid, pid, nid])
                
            return np.array(triplet_index)

        def __len__(self):
            return int(len(self.triplet_index) / self.batch_size)

        def on_epoch_end(self):
            if self.renew:
                self.triplet_index = self.__generate_triplet_index()
            if self.shuffle:
                np.random.shuffle(self.triplet_index)

        '''
        Retrieve bounds for specified index and batch size in self.config
        '''
        def __get_bounds__(self, idx):
            #Define bounds of the image range in current batch
            l_bound = idx*self.batch_size #left bound
            r_bound = (idx+1)*self.batch_size #right bound

            if r_bound > len(self.triplet_index):
                r_bound = len(self.triplet_index)
                # Keep batch size stable when length of images is not a multiple of batch size.
                l_bound = r_bound - self.batch_size
            return l_bound, r_bound


        def __getitem__(self, i):
            tic = time.time()
            ret = []
            l_bound, r_bound = self.__get_bounds__(i)
            for j in range(l_bound, r_bound):
                aid, pid, nid = self.triplet_index[j]
                anchor = self.images[aid]
                positive = self.images[pid]
                negative = self.images[nid]
                if self.images_as_path:
                    if self.image_size:
                        anchor = np.array(Image.open(anchor).resize(self.image_size))
                        positive = np.array(Image.open(positive).resize(self.image_size))
                        negative = np.array(Image.open(negative).resize(self.image_size))
                    else:
                        anchor = np.array(Image.open(anchor))
                        positive = np.array(Image.open(positive))
                        negative = np.array(Image.open(negative))
                ret.append([anchor, positive, negative])
            ret = np.array(ret)
            anchors, positives, negatives = ret[:, 0], ret[:, 1], ret[:, 2]
            dummy = np.zeros((self.batch_size, 1))
            toc = time.time()
            # print("Time it took to generate batch:", round(toc-tic, 3))
            return [anchors, positives, negatives], dummy

class ImageGenerator(keras.utils.Sequence):
        def __init__(self, image_paths, labels, batch_size = 64, shuffle = True, image_size = None, num_unique = None):
            self.batch_size = batch_size
            self.shuffle = shuffle
            self.image_size = image_size
            self.index = np.arange(0, len(image_paths))
            self.image_paths = image_paths
            self.labels = labels
            # self.unique_labels = np.unique(self.labels)
            self.num_unique = num_unique

        def __len__(self):
            return int(len(self.labels) / self.batch_size)

        def on_epoch_end(self):
            if self.shuffle:
                np.random.shuffle(self.index)

        '''
        Retrieve bounds for specified index and batch size in self.config
        '''
        def __get_bounds__(self, idx):
            #Define bounds of the image range in current batch
            l_bound = idx*self.batch_size #left bound
            r_bound = (idx+1)*self.batch_size #right bound

            if r_bound > len(self.image_paths):
                r_bound = len(self.image_paths)
                # Keep batch size stable when length of images is not a multiple of batch size.
                l_bound = r_bound - self.batch_size
            return l_bound, r_bound

        def __getitem__(self, i):
            X, Y = [], []
            l_bound, r_bound = self.__get_bounds__(i)
            for j in range(l_bound, r_bound):
                idx = self.index[j]
                img = Image.open(self.image_paths[idx])
                if self.image_size:
                    img = img.resize(self.image_size)
                img = np.array(img)
                X.append(img)
                label = np.zeros(self.num_unique)
                label[self.labels[j]] = 1
                Y.append(label)
            X = np.array(X)
            Y = np.array(Y)
            return X, Y
