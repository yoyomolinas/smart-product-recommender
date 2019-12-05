import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from tensorflow import keras
from PIL import Image
import base64
import utils

CONFIG_PATH = "config.json"
INPUT_SIZE = (256, 256)

DEBUG_FEATURES = 'temp_features.csv'

class API:
    def __init__(self, model_name = "bigxception_activation", dataset_name = 'boyner'):
        print("Loading feature extractor module..")
        self.config = self.load_config()
        
        # make assertions
        assert dataset_name in self.config['dataset'].keys(), "%s should be in config.json file"%dataset_name
        assert model_name in self.config['model'].keys(), "%s should be in config.json file"%model_name

        # load model
        self.model_name = model_name
        self.model_path = self.config['model'][self.model_name]
        self.model = keras.models.load_model(self.model_path)

        # load df from features/x.csv
        self.dataset_name = dataset_name
        self.dataset_path = self.config['dataset'][self.dataset_name]
        print("Loading data")
        self.df = pd.read_csv(self.dataset_path)
        self.index = np.array(self.df.index.tolist())

        # store all features as numpy array
        self.features = []
        print("Loading features")
        for feat_str in tqdm(self.df.feature.tolist()):
            self.features.append(eval(feat_str))
        self.features = np.array(self.features)



        # print("Shape of features:", self.features.shape)

        # lambda cosine distance
        self.__cos_dist = lambda vA, vB : np.dot(vA, vB) / (np.sqrt(np.dot(vA,vA)) * np.sqrt(np.dot(vB,vB)))

    def load_config(self):
        with open(CONFIG_PATH, 'r') as f:
            config_dict = json.load(f)
        return config_dict

    def get_closest_neighbors(base64_img, k = 16, min_price = 0, max_price = 1e6):
        """
        :param base64_img: image base64  
        :param k: k number of neighbors
        :param min_price: filter self.df accordingly
        :param max_price: filter self.df accordingly
        """
        # preprocess img
        img = self.decode_base_64(base64_img)
        img = utils.preprocess(Image.fromarray(img), size = INPUT_SIZE)
        return self._get_closest_neighbors(img, k = 16, min_price = 0, max_price = 1e6)
    
    def _get_closest_neighbors(self, img, k = 16, min_price = 0, max_price = 1e6):
        """
        :param img: numpy array 
        :param k: k number of neighbors
        :param min_price: filter self.df accordingly
        :param max_price: filter self.df accordingly
        """
        assert type(img) == np.ndarray, "img argument should be a numpy array but is %s"%type(img)

        # assign df to self.df
        df = self.df

        # infer features with model and image
        img_exp = np.expand_dims(img, axis = 0)
        img_exp
        categories, features = self.model.predict(img_exp)
        categories, features = np.squeeze(categories), np.squeeze(features)
        
        # filter category
        category = int(np.argmax(categories))
        df = df[df['category'] == category]

        # filter price
        df = df[(df['productprice'] > min_price) & (df['productprice'] < max_price)]

        # set index and filter features
        index = np.array(df.index) # set index
        search_features = self.features[index]

        # compute cosine distance between all features in df and img
        distances = np.array([self.__cos_dist(feat, features) for feat in search_features])
        distances_idx = np.argsort(distances)[::-1]
        index = index[distances_idx][:k] # k indices which will be input to data frame
        df = df.loc[index] # data frame with k elements

        # open images from df['local_path']
        # imgs_base_64 = []
        # for i, row in df.iterrows():
        #     neighbor_img_path = row['local_path']
        #     neighbor_img = Image.open(neighbor_img_path)
        #     neighbor_img = np.array(neighbor_img)
        #     neighbor_img_base_64 = self.encode_base_64(neighbor_img)
        #     imgs_base_64.append(neighbor_img_base_64)

        # df['base_64'] = imgs_base_64
        return df
    
    @staticmethod
    def encode_base_64(np_array):
        """
        :param np_array: image numpy array
        """
        base64_img = base64.b64encode(np_array)
        return base64_img
    
    @staticmethod
    def decode_base_64(base64_img):
        """
        :param base64_img: image base64 string
        """
        buffer = base64.b64decode(img)
        pil_img = Image.frombuffer(buffer)
        return pil_img

if __name__ == '__main__':
    pass