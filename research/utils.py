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
from PIL import ImageOps

def resampling_with_original_ratio(img, required_size, sample=Image.NEAREST):
    """Resizes the image to maintain the original aspect ratio by adding pixel padding where needed.
    For example, if your model's input tensor requires a square image but your image is landscape (and
    you don't want to reshape the image to fit), pass this function your image and the required square
    dimensions, and it returns a square version by adding the necessary amount of black pixels on the
    bottom-side only. If the original image is portrait, it adds black pixels on the right-side
    only.
    Args:
    img (:obj:`PIL.Image`): The image to resize.
    required_size (list): The pixel width and height [x, y] that your model requires for input.
    sample (int): A resampling filter for image resizing.
      This can be one of :attr:`PIL.Image.NEAREST` (recommended), :attr:`PIL.Image.BOX`,
      :attr:`PIL.Image.BILINEAR`, :attr:`PIL.Image.HAMMING`, :attr:`PIL.Image.BICUBIC`,
      or :attr:`PIL.Image.LANCZOS`. See `Pillow filters
      <https://pillow.readthedocs.io/en/stable/handbook/concepts.html#filters>`_.
    Returns:
    A 2-tuple with a :obj:`PIL.Image` object for the resized image, and a tuple of floats
    representing the aspect ratio difference between the original image and the returned image
    (x delta-ratio, y delta-ratio).
    """
    old_size = img.size
    # Resizing image with original ratio.
    resampling_ratio = min(
      required_size[0] / old_size[0],
      required_size[1] / old_size[1]
    )
    new_size = (
      int(old_size[0] * resampling_ratio),
      int(old_size[1] * resampling_ratio)
    )
    new_img = img.resize(new_size, sample)
    # Expand it to required size.
    delta_w = required_size[0] - new_size[0]
    delta_h = required_size[1] - new_size[1]
    padding = (0, 0, delta_w, delta_h)
    ratio = (new_size[0] / required_size[0], new_size[1] / required_size[1])
    return ImageOps.expand(new_img, padding)

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

    def list_files(self):
        return os.listdir(self.path)



