import pandas as pd

class FeatureExtractorAPI:
    def __init__(self, features_path):
        """
        :param features_path: A file that stores image paths, catgeories and features in a table (csv?).
        """
        self.df_path = features_path
        self.df = pd.read_csv(features_path)
        # TODO assert columns self.df has - possibly use an enforcer function to do this

    def get_closest_neighbors(self, image, tok_k = 10):
        """
        Function thar returns images found to have closest features to given image.
        :param image: numpy array
        :param top_k: return top_k images
        :return images: list of images as numpy arrays (or any other format?)
        """
        # TODO assert image is a numpy array
        raise NotImplementedError