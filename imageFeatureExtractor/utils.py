import os
import random
import numpy as np
from PIL import Image
import pandas as pd
from tqdm import tqdm
from itertools import permutations
import cv2
from os.path import join
import shutil

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

def load_data(label_path, resize = None, limit = None, images_as_path = False):
    """

    """
    assert os.path.isfile(label_path)
    X, Y = [], []
    category_index = {} # category index
    df = pd.read_csv(label_path, usecols = ['imagepath', 'labelid', 'labelname'])
    i = 0
    for fpath, cid, cname in tqdm(df.to_numpy()):
        if images_as_path:
            X.append(fpath)
        else:
            img = cv2.imread(fpath)
            if resize:
                img = cv2.resize(img, (resize[1], resize[0]))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_arr = np.array(img)
            if len(img_arr.shape) != 3:
                continue
            X.append(img_arr)
        Y.append(cid)
        category_index[cid] = cname
        if limit:
            if i > limit:
                break
        i += 1
    X = np.array(X)
    Y = np.array(Y)
    return X, Y, category_index

def split_by_class(x, y, ratio):
    """
    Split by class as test/train
    Return x_train, x_test, y_train, y_test
    """
    random.seed(2)
    classes, counts = np.unique(y, return_counts=True)
    test_cls = random.sample(list(classes), int(len(classes) * ratio))
    train_cls = list(set(classes).difference(set(test_cls)))

    # Split X/Y for training and testing
    train_index = list(filter(lambda i: y[i] in train_cls, range(len(y))))
    test_index = list(filter(lambda i: y[i] in test_cls, range(len(y))))
    return x[train_index], x[test_index], y[train_index], y[test_index]

def generate_triplet(x, y, ap_pairs=10, an_pairs=10):
    """
    Triplet generation for given images (x), and classes (y). A triplet consists of an anchor, a positive and negative. 
    The idea is to predict features that have the anchor closer to the positive and farther from the negative.
    :param x: array of images 
    :param y: array of class ids
    :return tuple: tuple of arrays of anchor, positives, and negatives
    """
    data_xy = tuple([x,y])

    triplet_pairs = []
    anchor = []
    pos = []
    neg = []
    for data_class in tqdm(sorted(set(data_xy[1]))):
        same_class_idx = np.where((data_xy[1] == data_class))[0]
        diff_class_idx = np.where(data_xy[1] != data_class)[0]
        num_positive_perms = min(len(list(permutations(same_class_idx,2))), ap_pairs)
        if num_positive_perms < 2:# or num_perms < ap_pairs:
            continue
        A_P_pairs = random.sample(list(permutations(same_class_idx,2)),k=num_positive_perms) #Generating Anchor-Positive pairs
        Neg_idx = random.sample(list(diff_class_idx),k=min(an_pairs, len(list(diff_class_idx))))

        A_P_len = len(A_P_pairs)
        Neg_len = len(Neg_idx)
        for ap in A_P_pairs[:A_P_len]:
            Anchor = data_xy[0][ap[0]]
            Positive = data_xy[0][ap[1]]
            for n in Neg_idx:
                Negative = data_xy[0][n]
                anchor.append(Anchor)
                pos.append(Positive)
                neg.append(Negative)
                
    # return np.array(triplet_pairs)
    return anchor, pos, neg

class DirectoryTree:
    """
    A class to ease operations in directories
    """
    def __init__(self, path = None, parent = None, depth = 0):
        self.parent = parent
        self.path = path
        self.directories = {}
        self.depth = depth
        if depth == 0:
            self.name = self.path
        else:
            self.name = self.path.split('/')[-1]

        if os.path.isfile(self.path):
            raise OSError('Please specify a directory not a file!')

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            # Iterate through all directories in self.path, and add to self.directories
            for dir in os.listdir(self.path):
                if os.path.isdir(join(self.path, dir)):
                    self.add(dir)

    def add(self, *names, overwrite = False):
        if not self.exists():
            raise OSError('This directory tree is no longer valid.')
        for name in names:
            if hasattr(self, name) and overwrite:
                self.directories[name].remove(hard = True)
                # raise OSError('path <%s> already exists in this file structure' % join(self.path, name))

            setattr(self, name, DirectoryTree(path = join(self.path, name), parent = self, depth = self.depth + 1))
            self.directories[name] = getattr(self, name)

    def print_all(self):
        if not self.exists():
            raise OSError('This directory tree is no longer valid.')
        cur_path = self.path.split('/')[-1]
        s = ''
        if self.depth != 0:
            s = '|'
            for i in range(self.depth):
                s += '___'

        print("%s%s"%(s, cur_path))
        for name, d in self.directories.items():
            d.print_all()

    def remove(self, hard = False):
        if not self.exists():
            raise OSError('This directory tree is no longer valid.')
        if hard:
            shutil.rmtree(self.path)
        else:
            os.rmdir(self.path)

        if self.parent is not None:
            delattr(self.parent, self.name)
            del self.parent.directories[self.name]

    def exists(self):
        return os.path.isdir(self.path)

