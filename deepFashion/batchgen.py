import random
import numpy as np
from itertools import permutations
from tensorflow import keras
import time
from PIL import Image
import cv2
import utils

# batch generator
class BatchGenerator(keras.utils.Sequence):
    """
    This batch generator generates batches of images, labels, attributes, and activation maps. 
    """
    def __init__(self,
                image_paths,
                bboxes,
                categories,
                attributes,
                eval_status,
                num_categories = 50,
                num_attributes = 10000,
                batch_size = 64,
                shuffle = True, 
                image_size = (128, 128),
                return_activation_map = True, 
                activation_map_size = (24, 24),
                activation_map_mode = 'box',
                mode = 'train'):
        """
        :param image_size: image_size in (width, height) format
        """
        assert mode in ['test', 'train', 'val']
        assert image_size[0] == image_size[1], \
            "Expected square image size please correct image_size argument accordingly"
        assert activation_map_size[0] == activation_map_size[1], \
            "Expected square activation map size please correct activation_map_size argument accordingly"
        self.mode = mode
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.image_size = image_size
        self.eval_status = np.array(eval_status)
        self.index = np.arange(0, len(image_paths))[self.eval_status == self.mode]
        np.random.shuffle(self.index)
        self.image_paths = image_paths
        self.bboxes = bboxes
        self.categories = categories
        self.attributes = attributes
        self.num_categories = num_categories
        self.num_attributes = num_attributes
        self.return_activation_map = return_activation_map
        self.activation_map_size = activation_map_size
        self.activation_map_mode=activation_map_mode
        self.morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        
    def __len__(self):
        """
        :return :Number of batches in this generator
        """
        return int(len(self.index) / self.batch_size)

    def on_epoch_end(self):
        """
        Function called in the end of every epoch.
        """
        if self.shuffle:
            np.random.shuffle(self.index)

    def __get_bounds__(self, idx):
        """
        Retrieve bounds for specified index
        :param idx: index 
        :return left bound, right bound:
        """
        #Define bounds of the image range in current batch
        l_bound = idx*self.batch_size #left bound
        r_bound = (idx+1)*self.batch_size #right bound

        if r_bound > len(self.image_paths):
            r_bound = len(self.image_paths)
            # Keep batch size stable when length of images is not a multiple of batch size.
            l_bound = r_bound - self.batch_size
        return l_bound, r_bound
    
    def get_attention_map(self, bbox, img_size, map_mode = 'gaussian'):
        """
        Return attention map of a given image. 
        This is either a 2d gaussian distribution centered at the center of the bounding box, 
        or a smoothed activation map of the bbox.
        :param bbox: bounding box in x1, x2, y1, y2 format where x refers to rows and y refers to columns
        :param size: size of activation map
        :param map_mode: one of ['box', 'smooth_box', 'gaussian']
        """
        assert map_mode in ['box', 'smooth_box', 'gaussian']
        x1, x2, y1, y2 = bbox
        act_arr = np.zeros((img_size[1], img_size[0]))
        if map_mode in ['smooth_box', 'box']:                
            act_arr[y1:y2, x1:x2] = 1
            if map_mode == 'smooth_box':
                act_arr = cv2.GaussianBlur(act_arr, (11, 11), 2, 2)
                act_arr = cv2.morphologyEx(act_arr, cv2.MORPH_CLOSE, self.morph_kernel)
        elif map_mode == 'gaussian':
            h, w = y2 - y1, x2 - x1
            x = np.expand_dims(np.sin(np.linspace(0, np.pi, h)), axis = -1)
            y = np.expand_dims(np.sin(np.linspace(0, np.pi, w)), axis = 0)
            act_arr[y1:y2, x1:x2] = x * y
        ret_img = Image.fromarray(act_arr)
        ret_img = utils.resampling_with_original_ratio(ret_img, self.activation_map_size)
        ret_arr = np.array(ret_img)
        return ret_arr
    
    def __getitem__(self, i):
        """
        Abstract function from Sequence class - called every iteration in model.fit_generator function.
        :param i: batch id
        :return X, [Y_map, Y_cat, Y_attr]
        """
        X, Y_map, Y_cat, Y_attr = [], [], [], []
        l_bound, r_bound = self.__get_bounds__(i)
        for j in range(l_bound, r_bound):
            idx = self.index[j]
            img = Image.open(self.image_paths[idx])
            if self.return_activation_map:
                act_map = self.get_attention_map(self.bboxes[idx], 
                                                    img_size=img.size,
                                                    map_mode = self.activation_map_mode)
            if self.image_size:
                img = utils.resampling_with_original_ratio(img, self.image_size)
            img_arr = np.array(img)
            cat_vec = np.zeros(self.num_categories)
            cat_vec[self.categories[idx]] = 1
            attr_vec = self.attributes[idx]
            X.append(img_arr)
            Y_cat.append(cat_vec)
            Y_attr.append(attr_vec)
            if self.return_activation_map:
                Y_map.append(act_map)
        X = np.array(X)
        Y_out = []
        if self.return_activation_map:
            Y_map = np.array(Y_map)
            Y_out.append(Y_map)
        Y_cat = np.array(Y_cat)
        Y_attr = np.array(Y_attr)
        Y_out.append(Y_cat)
        Y_out.append(Y_attr)
        
        return X, Y_out
    
