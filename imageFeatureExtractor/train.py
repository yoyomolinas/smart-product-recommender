import utils
import loss
import batchgen
import models
import callbacks
import numpy as np
from tensorflow import keras
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

from absl import app, flags, logging
from absl.flags import FLAGS

"""
This script trains a model on triplets.
Example usage: 
    python train.py --save_path progress/minix --epochs 10 --batch_size 16 --model_type 1 --input_size 100,133 --feature_size 64 --overwrite
"""

DEFAULT_LABEL_PATH = "data/labels/lcwaikiki100k_labels.csv"
DEFAULT_SAVE_PATH = "progress/test/"
DEFAULT_NUM_PAIRS = 50
DEFAULT_FEATURE_SIZE = 64
DEFAULT_BATCH_SIZE = 32
DEFAULT_NUM_EPOCHS = 30
DEFAULT_IMAGE_SIZE = [300, 400] # width, height
DEFAULT_MODEL_TYPE = 1

flags.DEFINE_string('label_path', DEFAULT_LABEL_PATH, 'labels to load')
flags.DEFINE_string('save_path', DEFAULT_SAVE_PATH, 'path to save checkpoints and logs')
flags.DEFINE_boolean('overwrite', False, 'Overwrite given save path')
flags.DEFINE_integer('num_ap_pairs', DEFAULT_NUM_PAIRS, 'number of anchor positive pairs')
flags.DEFINE_integer('num_an_pairs', DEFAULT_NUM_PAIRS, 'number of anchor negative pairs')
flags.DEFINE_integer('feature_size', DEFAULT_FEATURE_SIZE, 'number of features')
flags.DEFINE_integer('batch_size', DEFAULT_BATCH_SIZE, 'batch size')
flags.DEFINE_list('input_size', DEFAULT_IMAGE_SIZE, 'input size in (width, height) format')
flags.DEFINE_integer('epochs', DEFAULT_NUM_EPOCHS, 'number of epochs')
flags.DEFINE_integer('model_type', DEFAULT_MODEL_TYPE, 'integer model type - %s'%str(models.ENUM_MODELS_DICT))

def main(_argv):
    assert FLAGS.model_type in models.ENUM_MODELS_DICT.keys()
    input_size = (int(FLAGS.input_size[0]) , int(FLAGS.input_size[1])) # (width, height)
    input_shape = (int(FLAGS.input_size[1]), int(FLAGS.input_size[0]), 3)
    logging.info("Loading data")
    # Load data
    X, Y, index = utils.load_data(FLAGS.label_path, resize = input_size, limit = None, images_as_path = True)
    
    # Split train test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
    
    logging.info("Creating batch train/test generators")
    # Define Triplet Generator
    tripletgen_train = batchgen.TripletGenerator(X_train, Y_train, ap_pairs = FLAGS.num_ap_pairs, an_pairs = FLAGS.num_an_pairs, batch_size = FLAGS.batch_size, shuffle = True, renew = True, images_as_path = True, image_size = input_size)
    tripletgen_test = batchgen.TripletGenerator(X_test, Y_test, ap_pairs = FLAGS.num_ap_pairs, an_pairs = FLAGS.num_an_pairs, batch_size = FLAGS.batch_size, shuffle = False, renew = False, images_as_path = True, image_size = input_size)

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
    try:
        model.fit_generator(
            tripletgen_train,
            steps_per_epoch = 3000,
            validation_data=tripletgen_test, 
            validation_steps = 100,
            max_queue_size = 1000,
            epochs=FLAGS.epochs, 
            verbose = 1,
            use_multiprocessing = True,
            workers = 6,
            callbacks = callbacks.generate_keras_callbacks(FLAGS.save_path, overwrite = FLAGS.overwrite))

    except Exception as e:
        raise e
    finally:
        logging.info("Saving model")
        # model.save_weights(FLAGS.save_path)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass