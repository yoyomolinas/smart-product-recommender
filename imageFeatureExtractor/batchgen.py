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
            if self.shuffle:
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

        def __getitem__(self, i):
            tic = time.time()
            ret = []
            for j in range(i, i + self.batch_size):
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
