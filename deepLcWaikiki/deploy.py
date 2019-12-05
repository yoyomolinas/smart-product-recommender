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
flags.DEFINE_integer('output_size', None, 'number of classes')
flags.mark_flag_as_required('weights_path')
flags.mark_flag_as_required('save_path')
flags.mark_flag_as_required('model_type')


def main(_argv):
    assert FLAGS.model_type in models.ENUM_MODELS_DICT.keys()
    input_shape = (int(FLAGS.input_size[1]), int(FLAGS.input_size[0]), 3)
    logging.info("Creating network")
    # Prepare network
    network_input = keras.layers.Input(input_shape, name='input')

    if FLAGS.output_size:
        DNN = models.ENUM_MODELS_DICT[FLAGS.model_type](
            input_tensor = network_input,
            feature_size = FLAGS.feature_size,
            output_size = FLAGS.output_size,
            output_activation = 'softmax')

        # Individual outputs
        embed = DNN.get_layer('embeddings').output
        classif = DNN.get_layer('classification').output
        # Setup and compile model
        model = keras.models.Model(inputs=network_input, outputs=classif)
        model.load_weights(FLAGS.weights_path)
        model = keras.models.Model(inputs=network_input, outputs=embed)

    else:
        DNN = models.ENUM_MODELS_DICT[FLAGS.model_type](
            input_shape = input_shape,
            feature_size = FLAGS.feature_size)

        model = keras.models.Model(inputs=network_input, outputs=DNN(network_input))
        model.load_weights(FLAGS.weights_path)

    model.summary()

    model.save(FLAGS.save_path)
    logging.info("Saved final version of the model into %s"%FLAGS.save_path)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass