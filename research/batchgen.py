import random
import numpy as np
from itertools import permutations
from tensorflow import keras
import time
from PIL import Image
import cv2
import utils
from imgaug import augmenters as iaa

class BatchGenerator(keras.utils.Sequence):
    """
    This batch generator generates batches of augmented images, labels, and attributes.
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
                jitter = False,
                crop = False,
                mode = 'train'):
        """
        :param image_size: image_size in (width, height) format
        """
        assert mode in ['test', 'train', 'val']
        assert image_size[0] == image_size[1], \
            "Expected square image size please correct image_size argument accordingly"
        self.mode = mode
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.image_size = image_size
        self.eval_status = np.array(eval_status)
        self.index = np.arange(0, len(image_paths))[self.eval_status == self.mode]
        np.random.seed(1)
        np.random.shuffle(self.index)
        self.image_paths = image_paths
        self.bboxes = bboxes
        self.categories = categories
        self.attributes = attributes
        self.num_categories = num_categories
        self.num_attributes = num_attributes
        self.aug_pipe = self.get_aug_pipeline(p = 0.5)  
        self.jitter = jitter
        self.crop = crop
        
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

    def preprocess(self, image, bbox, size):
        """
        :param image: PIL image
        :param bbox: bounding box in (x1, y1, x2, y2) format
        :return image: numpy array
        """
        temp_image = image
        if self.crop:
            temp_image = temp_image.crop(bbox)
        temp_image = utils.resampling_with_original_ratio(temp_image, self.image_size)
        temp_image = np.array(temp_image)
        if self.jitter:
            temp_image = self.aug_pipe.augment_image(temp_image)
        return temp_image

    def get_aug_pipeline(self, p = 0.2):
        # Helper Lambda

        sometimes = lambda aug: iaa.Sometimes(p, aug)

        aug_pipe = iaa.Sequential(
            [
                iaa.SomeOf(
                    (1, 2),
                    [
                        # sometimes(iaa.Fliplr(1.)),  # horizontally flip 50% of all images
                        sometimes(iaa.Crop(percent=(0, 0.15))),  # crop images by 0-10% of their height/width
                        sometimes(iaa.Affine(translate_percent={"x": (-0.15, 0.15), "y": (-0.15, 0.15)}))
                    ],
                    random_order=True
                ),
                iaa.OneOf(
                    [
                        sometimes(iaa.Multiply((0.5, 0.5), per_channel=0.5)),
                        iaa.GaussianBlur((0, 3.0)),  # blur images with a sigma between 0 and 3.0
                        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.04 * 255), per_channel=0.5),
                        
                    ]
                )
            ],
            random_order=True
        )

        return aug_pipe  

    def __getitem__(self, i):
        """
        Abstract function from Sequence class - called every iteration in model.fit_generator function.
        :param i: batch id
        :return X, [Y_map, Y_cat, Y_attr]
        """
        X, Y_cat, Y_attr = [], [], []
        l_bound, r_bound = self.__get_bounds__(i)
        for j in range(l_bound, r_bound):
            idx = self.index[j]
            img = Image.open(self.image_paths[idx])
            bbox = (self.bboxes[idx][0], self.bboxes[idx][2], self.bboxes[idx][1], self.bboxes[idx][3]) # (x1, y1, x2, y2)
            img_arr = self.preprocess(img, bbox, size= self.image_size)
            cat_vec = np.zeros(self.num_categories)
            cat_vec[self.categories[idx]] = 1
            attr_vec = self.attributes[idx]
            X.append(img_arr)
            Y_cat.append(cat_vec)
            Y_attr.append(attr_vec)
        X = np.array(X)
        Y_out = [np.array(Y_cat), np.array(Y_attr)]
        return X, Y_out