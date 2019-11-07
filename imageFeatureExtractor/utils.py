import os
import random
import numpy as np
from PIL import Image
import pandas as pd
from tqdm import tqdm
from itertools import permutations

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

def load_data(label_path, resize = None, limit = None):
    """

    """
    assert os.path.isfile(label_path)
    X, Y = [], []
    category_index = {} # category index
    df = pd.read_csv(label_path, usecols = ['imagepath', 'labelid', 'labelname'])
    i = 0
    for fpath, cid, cname in tqdm(df.to_numpy()):
        img = Image.open(fpath)
        if resize:
            img = img.resize(resize, Image.NEAREST)
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

