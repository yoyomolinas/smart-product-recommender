import utils
import loss
import batchgen
import models
import numpy as np
from tensorflow import keras
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

from absl import app, flags, logging
from absl.flags import FLAGS

"""
This script deploys a model trained on triplets.
Example usage: 
    python deploy.py --weights_path progress/pretrn_imagenet_mobilv1/ckpt/weights. --save_path deploy/pretrn_imagenet_mobilv1/model.hdf5 --input_size 100,133 --model_type 3
"""


DEFAULT_FEATURE_SIZE = 64
DEFAULT_IMAGE_SIZE = [300, 400] # width, height

flags.DEFINE_string('weights_path', None, 'keras model weights')
flags.DEFINE_string('save_path', None, 'path to save model')
flags.DEFINE_list('input_size', DEFAULT_IMAGE_SIZE, 'input size in (width, height) format')
flags.DEFINE_integer('model_type', None, 'integer model type - %s'%str(models.ENUM_MODELS_DICT))
flags.DEFINE_integer('feature_size', DEFAULT_FEATURE_SIZE, 'number of features')
flags.mark_flag_as_required('weights_path')
flags.mark_flag_as_required('save_path')
flags.mark_flag_as_required('model_type')


def main(_argv):
    assert FLAGS.model_type in models.ENUM_MODELS_DICT.keys()
    input_shape = (int(FLAGS.input_size[1]), int(FLAGS.input_size[0]), 3)
    logging.info("Creating network")
    # Prepare network
    anchor_input = keras.layers.Input(input_shape, name='anchor_input')

    # Shared embedding layer for positive and negative items        
    Shared_DNN = models.ENUM_MODELS_DICT[FLAGS.model_type](input_shape, feature_size = FLAGS.feature_size)

    # Individual outputs
    encoded_anchor = Shared_DNN(anchor_input)

    # Merged output layer

    # Setup and compile model
    model = keras.models.Model(inputs=anchor_input, outputs=encoded_anchor)
    model.load_weights(FLAGS.weights_path)

    model.summary()

    model.save(FLAGS.save_path)
    logging.info("Saved final version of the model into %s"%FLAGS.save_path)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass