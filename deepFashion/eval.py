import numpy as np
from os.path import join
from tensorflow import keras
from PIL import Image
import random
from tqdm import tqdm
import pickle

import utils
from batchgen import BatchGenerator
import models

from absl import app, flags, logging
from absl.flags import FLAGS

"""
This script evaluates a deployed model
Example usage: 
    python eval.py --model_path deploy/mobil-v2-pre-crop.hdf5 --input_size 256,256 --crop
"""

DEFAULT_IMAGE_SIZE = [256, 256] # width, height

flags.DEFINE_string('model_path', None, 'path to deployed hdf5 file - should conatin entire model')
flags.DEFINE_boolean('crop', False, 'Eval on crops of clothes')
flags.DEFINE_list('input_size', DEFAULT_IMAGE_SIZE, 'input size in (width, height) format')
flags.DEFINE_integer('num_query', 144, 'number of images to query for evaluating retreival - default to 144')
flags.DEFINE_integer('num_augments', 20, 'number of augmentations to apply to each query image - default to 20')
flags.DEFINE_integer('batch_idx', 100, 'batch id')

def main(_):
    input_size = (int(FLAGS.input_size[0]) , int(FLAGS.input_size[1])) # (width, height)
    input_shape = (int(FLAGS.input_size[1]), int(FLAGS.input_size[0]), 3)

    # load data
    logging.info("Loading data")
    dt = utils.DirectoryTree("data/Category and Attribute Prediction Benchmark/")
    with open(join(dt.Anno.path, 'meta.pickle'), 'rb' ) as f:
        data = pickle.load(f)

    # load model
    logging.info("Loading model")
    model = keras.models.load_model(FLAGS.model_path)

    # create batchgen
    no_jitter_std_args_dict = dict(
        image_paths = list(map(lambda path: join(dt.Img.path, path), data['img_names'])), 
        bboxes = data['bbox_coords'],
        categories=data['cat_labels'],
        attributes=data['attr_labels'],
        eval_status=data['eval_status'],
        batch_size=32,
        image_size=input_size,
        shuffle = True,
        jitter = False,
        crop = FLAGS.crop,
        mode = 'test'
    )

    retreival_args_dict = dict(
        image_paths = list(map(lambda path: join(dt.Img.path, path), data['img_names'])), 
        bboxes = data['bbox_coords'],
        categories=data['cat_labels'],
        attributes=data['attr_labels'],
        eval_status=data['eval_status'],
        batch_size=FLAGS.num_query,
        image_size=input_size,
        shuffle = True,
        jitter = True,
        crop = FLAGS.crop,
        mode = 'test'
    )

    std_gen = BatchGenerator(**no_jitter_std_args_dict)
    ret_gen = BatchGenerator(**retreival_args_dict)

    logging.info("Forming dataset with duplicate augmented images")
    # Form a dataset with duplicate augmented images
    X_anchor = []
    Y_anchor_true = []
    X_query, _ = ret_gen.__getitem__(FLAGS.batch_idx)
    Y_query_true = [i for i in range(FLAGS.num_query)]
    for i in tqdm(range(FLAGS.num_augments)):
        X, _ = ret_gen.__getitem__(FLAGS.batch_idx)
        X_anchor.extend(X)
        Y_anchor_true.extend([i for i in range(FLAGS.num_query)])
        
    X_anchor = np.array(X_anchor)
    Y_anchor_true = np.array(Y_anchor_true)

    # predict for query and anchor images
    logging.info("Predicting query images")
    Y_query_pred = model.predict(X_query.astype(np.float32))
    logging.info("Predicting anchor images")
    Y_anchor_pred = model.predict(X_anchor.astype(np.float32))

    Y_anchor_pred_cats, Y_anchor_pred_attrs = Y_anchor_pred
    Y_query_pred_cats, Y_query_pred_attrs = Y_query_pred

    # define distance metric
    cos = lambda vA, vB : np.dot(vA, vB) / (np.sqrt(np.dot(vA,vA)) * np.sqrt(np.dot(vB,vB))) 

    # num_cols = 12
    # fig, axes = plt.subplots(1, num_cols, figsize = (20, 2))
    # plt.title("Query images")
    # axes = axes.flatten()
    # for i, img in enumerate(X_query[:12]):
    #     axes[i].imshow(img)
    #     axes[i].set_xticks([])
    #     axes[i].set_yticks([])

    # fig, axes = plt.subplots(n, num_cols, figsize = (20, 20))
    # plt.title("Retreival images")
    logging.info("Computing retreival accuracy for %i images"%FLAGS.num_query)
    results = []
    for col, (query_true, query_pred_attr) in tqdm(enumerate(zip(Y_query_true, Y_query_pred_attrs))):
        dist = [cos(query_pred_attr, anchor_pred_attr) for anchor_pred_attr in Y_anchor_pred_attrs]
        idx = np.argsort(dist, axis = 0)[::-1]
        temp = Y_anchor_true[idx][:FLAGS.num_augments]
        temp_imgs = X_anchor[idx][:FLAGS.num_augments]
        acc = sum(temp == query_true) / len(temp)
        results.append(acc)
        # if num_cols > col:
        #     for row, img in enumerate(temp_imgs):
        #         axes[row, col].imshow(img)
        #         axes[row, col].set_xticks([])
        #         axes[row, col].set_yticks([])

    # report evaluation metrics on entire test set
    logging.info("Evaluating model on test set : %i images "%int(len(std_gen) * 32))
    _, _, _, cat_recall, cat_precision, attr_recall, attr_precision = model.evaluate_generator(std_gen, verbose = 1)

    logging.info("----------------Results----------------")
    logging.info("Model path : %s"%FLAGS.model_path)
    logging.info("Clothes cropped : %s"%str(FLAGS.crop))
    logging.info("Model input size : %s"%str(input_size))
    logging.info("Number of images queried : %i"%FLAGS.num_query)
    logging.info("Number of augmentations applied to each query image : %i"%FLAGS.num_augments)
    logging.info("Batch idx utilized : %i"%FLAGS.batch_idx)
    logging.info("\n")
    logging.info("-----------Evaluation Results-----------")
    logging.info("Categories Recall: %.3f"%cat_recall)
    logging.info("Categories Precision: %.3f"%cat_precision)
    logging.info("Attributes Recall: %.3f"%attr_recall)
    logging.info("Attributes Precision: %.3f"%attr_precision)
    logging.info("----------------------------------------")
    logging.info("\n")
    logging.info("-----------Retreival Results------------")
    logging.info("Distance metric: %s"%"Cosine")
    logging.indo("Average retreival accuracy : %.4f"%np.mean(results))
    logging.info("----------------------------------------")
    logging.info("\n")

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass