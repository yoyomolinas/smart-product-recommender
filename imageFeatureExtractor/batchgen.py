import random
import numpy as np
from itertools import permutations
from tensorflow import keras

class TripletGenerator(keras.utils.Sequence):
        def __init__(self, X, Y, ap_pairs= 10, an_pairs = 10, batch_size = 64):
            self.batch_size = batch_size
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
            return int(len(self.labels) / self.batch_size)

        def on_epoch_end(self):
            np.random.shuffle(self.triplet_index)

        def __getitem__(self, i):
            ret = []
            for j in range(i, i + self.batch_size):
                aid, pid, nid = self.triplet_index[j]
                anchor = self.images[aid]
                positive = self.images[pid]
                negative = self.images[nid]
                ret.append([anchor, positive, negative])
            ret = np.array(ret)
            anchors, positives, negatives = ret[:, 0], ret[:, 1], ret[:, 2]
            dummy = np.zeros((self.batch_size, 1))
            return [anchors, positives, negatives], dummy
