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
DEFAULT_NUM_PAIRS = 70
DEFAULT_FEATURE_SIZE = 64
# DEFAULT_OUTPUT_SIZE = None
DEFAULT_BATCH_SIZE = 32
DEFAULT_NUM_EPOCHS = 30
DEFAULT_IMAGE_SIZE = [300, 400] # width, height
DEFAULT_MODEL_TYPE = 1

flags.DEFINE_string('label_path', DEFAULT_LABEL_PATH, 'labels to load')
flags.DEFINE_string('save_path', DEFAULT_SAVE_PATH, 'path to save checkpoints and logs')
flags.DEFINE_boolean('overwrite', False, 'Overwrite given save path')
flags.DEFINE_string('from_ckpt', None, 'path to continue training on checkpoint')
flags.DEFINE_integer('num_ap_pairs', DEFAULT_NUM_PAIRS, 'number of anchor positive pairs')
flags.DEFINE_integer('num_an_pairs', DEFAULT_NUM_PAIRS, 'number of anchor negative pairs')
flags.DEFINE_integer('feature_size', DEFAULT_FEATURE_SIZE, 'number of features')
# flags.DEFINE_integer('output_size', DEFAULT_OUTPUT_SIZE, 'output size - use this if you want to train a classififcation model')
flags.DEFINE_integer('batch_size', DEFAULT_BATCH_SIZE, 'batch size')
flags.DEFINE_list('input_size', DEFAULT_IMAGE_SIZE, 'input size in (width, height) format')
flags.DEFINE_integer('epochs', DEFAULT_NUM_EPOCHS, 'number of epochs')
flags.DEFINE_integer('model_type', DEFAULT_MODEL_TYPE, 'integer model type - %s'%str(models.ENUM_MODELS_DICT))


def main(_argv):
    assert FLAGS.model_type in models.ENUM_MODELS_DICT.keys()
    assert not ((FLAGS.overwrite) and (FLAGS.from_ckpt is not None))
    input_size = (int(FLAGS.input_size[0]) , int(FLAGS.input_size[1])) # (width, height)
    input_shape = (int(FLAGS.input_size[1]), int(FLAGS.input_size[0]), 3)
    logging.info("Loading data")
    # Load data
    X, Y, index = utils.load_data(FLAGS.label_path, resize = input_size, limit = None, images_as_path = True)
    num_unique = len(np.unique(Y))
    # Split train test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
    
    logging.info("Creating batch train/test generators")
    # Define Triplet Generator
    tripletgen_train = batchgen.ImageGenerator(X_train, Y_train, batch_size = FLAGS.batch_size, shuffle = True, image_size = input_size, num_unique = num_unique)
    tripletgen_test = batchgen.ImageGenerator(X_test, Y_test, batch_size = FLAGS.batch_size, shuffle = False, image_size = input_size, num_unique = num_unique)

    logging.info("Creating network")
    # Prepare network
    network_input = keras.layers.Input(input_shape, name='network_input')

    # Shared embedding layer for positive and negative items
    DNN = models.ENUM_MODELS_DICT[FLAGS.model_type](
        input_tensor = network_input,
        feature_size = FLAGS.feature_size,
        output_size = num_unique,
        output_activation = 'softmax')

    # Define optimizer
    adam_optim = keras.optimizers.Adam(lr=0.0001, beta_1=0.9, beta_2=0.999)
    
    # Setup and compile model
    model = keras.models.Model(inputs=network_input, outputs=DNN.get_layer('classification').output)
    model.compile(loss='categorical_crossentropy', optimizer=adam_optim, metrics = ['categorical_accuracy'])

    model.summary()

    if FLAGS.from_ckpt is not None:
        logging.info("Loading weights from %s"%FLAGS.from_ckpt)
        model.load_weights(FLAGS.from_ckpt)

    logging.info("Starting training")
    model.fit_generator(
        tripletgen_train,
        steps_per_epoch = 30000,
        validation_data=tripletgen_test, 
        validation_steps = 3000,
        max_queue_size = 1000,
        epochs=FLAGS.epochs, 
        verbose = 1,
        use_multiprocessing = True,
        workers = 4,
        callbacks = callbacks.generate_keras_callbacks(FLAGS.save_path, 
        overwrite = FLAGS.overwrite))

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass