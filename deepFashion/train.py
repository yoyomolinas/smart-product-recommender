from os.path import join
import pickle
import numpy as np
from tensorflow import keras
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

from absl import app, flags, logging
from absl.flags import FLAGS

import utils
import models 
from batchgen import BatchGenerator
import callbacks

"""
This script trains a model on triplets.
Example usage: 
    python train.py --save_path progress/mobil-pre- --epochs 100 --batch_size 32 --model_type 1 --input_size 256,256 --augment --loss_weights 1,100 --crop
"""

DEFAULT_SAVE_PATH = "progress/test/"
# DEFAULT_OUTPUT_SIZE = None
DEFAULT_BATCH_SIZE = 32
DEFAULT_NUM_EPOCHS = 30
DEFAULT_IMAGE_SIZE = [256, 256] # width, height
DEFAULT_MODEL_TYPE = 0
DEFAULT_LOSS_WEIGHTS= ['0.5', '0.5']

flags.DEFINE_string('save_path', DEFAULT_SAVE_PATH, 'path to save checkpoints and logs')
flags.DEFINE_boolean('overwrite', False, 'Overwrite given save path')
flags.DEFINE_boolean('augment', False, 'Apply image augmentation')
flags.DEFINE_boolean('crop', False, 'Train on crops of clothes')
flags.DEFINE_string('from_ckpt', None, 'path to continue training on checkpoint')
flags.DEFINE_integer('batch_size', DEFAULT_BATCH_SIZE, 'batch size')
flags.DEFINE_list('input_size', DEFAULT_IMAGE_SIZE, 'input size in (width, height) format')
flags.DEFINE_list('loss_weights', DEFAULT_LOSS_WEIGHTS, 'loss weights size in (w1, w2) format')
flags.DEFINE_integer('epochs', DEFAULT_NUM_EPOCHS, 'number of epochs')
flags.DEFINE_integer('model_type', DEFAULT_MODEL_TYPE, 'integer model type - %s'%str(models.ENUM_MODELS_DICT))

def main(_argv):
    assert FLAGS.model_type in models.ENUM_MODELS_DICT.keys()
    assert not ((FLAGS.overwrite) and (FLAGS.from_ckpt is not None))
    input_size = (int(FLAGS.input_size[0]) , int(FLAGS.input_size[1])) # (width, height)
    input_shape = (int(FLAGS.input_size[1]), int(FLAGS.input_size[0]), 3)
    loss_weights = (float(FLAGS.loss_weights[0]), float(FLAGS.loss_weights[1]))
    logging.info("Loading data")
    # Load data
    dt = utils.DirectoryTree("data/Category and Attribute Prediction Benchmark/")
    with open(join(dt.Anno.path, 'meta.pickle'), 'rb' ) as f:
        data = pickle.load(f)

    # Define batch generators
    gen_train_args_dict = dict(
        image_paths = list(map(lambda path: join(dt.Img.path, path), data['img_names'])), 
        bboxes = data['bbox_coords'],
        categories=data['cat_labels'],
        attributes=data['attr_labels'],
        eval_status=data['eval_status'],
        batch_size=FLAGS.batch_size,
        image_size=input_size,
        shuffle = True,
        jitter = FLAGS.augment,
        crop = FLAGS.crop,
        mode = 'train')

    gen_test_args_dict = dict(
        image_paths = list(map(lambda path: join(dt.Img.path, path), data['img_names'])), 
        bboxes = data['bbox_coords'],
        categories=data['cat_labels'],
        attributes=data['attr_labels'],
        eval_status=data['eval_status'],
        batch_size=FLAGS.batch_size,
        image_size=input_size,
        shuffle = False,
        jitter = False,
        crop = FLAGS.crop,
        mode = 'test'
    )

    logging.info("Creating batch generators")
    gen_train = BatchGenerator(**gen_train_args_dict)
    gen_test = BatchGenerator(**gen_test_args_dict)

    # Prepare network
    model = models.ENUM_MODELS_DICT[FLAGS.model_type](input_shape=input_shape)
    
    # Setup and compile model
    model.compile(optimizer = 'adam', 
                loss = {'categories':'categorical_crossentropy', 'attributes':'binary_crossentropy'},
                loss_weights = {'categories':loss_weights[0], 'attributes':loss_weights[1]},
                metrics = {
                    'categories':['categorical_accuracy', keras.metrics.Recall(), keras.metrics.Precision()], 
                    'attributes':['binary_accuracy', keras.metrics.Recall(), keras.metrics.Precision()]})
    logging.info("Compiled model with loss weights:%s"%str(loss_weights))
    model.summary()     

    if FLAGS.from_ckpt is not None:
        logging.info("Loading weights from %s"%FLAGS.from_ckpt)
        model.load_weights(FLAGS.from_ckpt)

    logging.info("Starting training")
    model.fit_generator(
        gen_train,
        steps_per_epoch = 8000,
        validation_data=gen_test, 
        validation_steps = 800,
        epochs=FLAGS.epochs, 
        verbose = 1,
        use_multiprocessing = True,
        workers = 4,
        callbacks = callbacks.generate_keras_callbacks(
            FLAGS.save_path,
            overwrite = FLAGS.overwrite))

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass