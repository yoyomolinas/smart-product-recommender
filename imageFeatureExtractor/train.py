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
This script trains a model on triplets.
Example usage: 
    python train.py --save_path ../progress/minix/model.hdf5 --epochs 60 --batch_size 32
"""

# Example command: 

DEFAULT_LABEL_PATH = "data/labels/lcwaikiki_labels.csv"
DEFAULT_SAVE_PATH = "../progress/model.hdf5"
DEFAULT_NUM_PAIRS = 150
DEFAULT_FEATURE_SIZE = 64
DEFAULT_BATCH_SIZE = 32
DEFAULT_NUM_EPOCHS = 30
DEFAULT_IMAGE_SIZE = (300, 400) # width, height
DEFAULT_MODEL_TYPE = 1

flags.DEFINE_string('label_path', DEFAULT_LABEL_PATH, 'labels to load')
flags.DEFINE_string('save_path', DEFAULT_SAVE_PATH, 'path to save model')
flags.DEFINE_integer('num_ap_pairs', DEFAULT_NUM_PAIRS, 'number of anchor positive pairs')
flags.DEFINE_integer('num_an_pairs', DEFAULT_NUM_PAIRS, 'number of anchor negative pairs')
flags.DEFINE_integer('feature_size', DEFAULT_FEATURE_SIZE, 'number of features')
flags.DEFINE_integer('batch_size', DEFAULT_BATCH_SIZE, 'batch size')
flags.DEFINE_integer('epochs', DEFAULT_NUM_EPOCHS, 'number of epochs')
flags.DEFINE_integer('model_type', DEFAULT_MODEL_TYPE, 'integer model type - %s'%str(models.ENUM_MODELS_DICT))

def main(_argv):
    input_shape = (DEFAULT_IMAGE_SIZE[1], DEFAULT_IMAGE_SIZE[0], 3)
    logging.info("Loading data")
    # Load data
    X, Y, index = utils.load_data(FLAGS.label_path, resize = DEFAULT_IMAGE_SIZE, limit = None)

    # Split train test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)

    logging.info("Creating batch train/test generators")
    # Define Triplet Generator
    tripletgen_train = batchgen.TripletGenerator(X_train, Y_train, ap_pairs = FLAGS.num_ap_pairs, an_pairs = FLAGS.num_an_pairs, batch_size = FLAGS.batch_size)
    tripletgen_test = batchgen.TripletGenerator(X_test, Y_test, ap_pairs = FLAGS.num_ap_pairs, an_pairs = FLAGS.num_an_pairs, batch_size = FLAGS.batch_size)

    logging.info("Creating network")
    # Prepare network
    anchor_input = keras.layers.Input(input_shape, name='anchor_input')
    positive_input = keras.layers.Input(input_shape, name='positive_input')
    negative_input = keras.layers.Input(input_shape, name='negative_input')

    # Shared embedding layer for positive and negative items
    Shared_DNN = models.ENUM_MODELS_DICT[FLAGS.model_type](input_shape, feature_size = FLAGS.feature_size)

    # Individual outputs
    encoded_anchor = Shared_DNN(anchor_input)
    encoded_positive = Shared_DNN(positive_input)
    encoded_negative = Shared_DNN(negative_input)

    # Merged output layer
    merged_vector = keras.layers.concatenate([encoded_anchor, encoded_positive, encoded_negative], axis=-1, name='merged_layer')

    # Define optimizer
    adam_optim = keras.optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999)

    # Setup and compile model
    model = keras.models.Model(inputs=[anchor_input,positive_input, negative_input], outputs=merged_vector)
    model.compile(loss=loss.triplet_loss, optimizer=adam_optim)

    model.summary()

    logging.info("Starting training")
    # Train model
    model.fit_generator(
        tripletgen_train,
        validation_data=tripletgen_test, 
        epochs=FLAGS.epochs, verbose = 1)

    logging.info("Saving model")
    model.save(FLAGS.save_path)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass