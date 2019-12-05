import pandas as pd
from tqdm import tqdm
from PIL import Image
import numpy as np
from tensorflow import keras

from absl import app, flags, logging
from absl.flags import FLAGS

import utils

"""
This script extracts features for given dataset.
Example usage: 
    python extract.py --dataset boyner --model models/bigx.hdf5 --batch_size 1000 --input_size 256,256
"""

DEFAULT_BATCH_SIZE = 1000
DEFAULT_IMAGE_SIZE = [256, 256]

DATASET_PATH_DICT = {
    'boyner':['data/labels/boyner.csv'],
    'lcwaikiki':['data/labels/lcwaikiki.csv'],
    'all': ['data/labels/boyner.csv', 'data/labels/lcwaikiki.csv']}

SAVE_TO_PATH_DICT = {
    'boyner':'data/features/boyner.csv',
    'lcwaikiki':'data/features/lcwaikiki.csv',
    'all': 'data/features/all.csv'}


flags.DEFINE_integer('batch_size', DEFAULT_BATCH_SIZE, 'batch size should not be too large as to exceed RAM capacity, dont use if in doubt')
flags.DEFINE_string('dataset', None, 'should be one of %s'%str(list(DATASET_PATH_DICT.keys())))
flags.DEFINE_string('model', None, "path to model")
# flags.DEFINE_string('save_to', None, "put any path here, recommendded is : data/features/x.csv")
flags.DEFINE_list('input_size', DEFAULT_IMAGE_SIZE, 'input size in (width, height) format')

flags.mark_flag_as_required('dataset')
flags.mark_flag_as_required('model')
# flags.mark_flag_as_required('save_to')

def main(__):
    assert FLAGS.dataset in DATASET_PATH_DICT.keys(), 'dataset should be one of %s'%str(list(DATASET_PATH_DICT.keys()))
    input_size = (int(FLAGS.input_size[0]) , int(FLAGS.input_size[1])) # (width, height)
    df_list = []
    logging.info("Extracting features for : %s"%FLAGS.dataset)
    for dataset_path in DATASET_PATH_DICT[FLAGS.dataset]:
        logging.info("Extracting features from path : %s"%dataset_path)
        df = pd.read_csv(dataset_path)
        index = df.index.tolist()
        batch = []
        ret_dict = {col: [] for col in df.columns}
        ret_dict.update({'category':[], 'feature':[]})
        model = keras.models.load_model(FLAGS.model)
        for i in tqdm(index):
            row = df.iloc[i, :]
            img = Image.open(row['local_path'])
            img_prep = utils.preprocess(img, size = input_size).convert("RGB")
            img_prep_numpy = np.array(img_prep)
            assert len(img_prep_numpy.shape) == 3, "numpy image not 3 dimensional : %s"%str(img_prep_numpy.shape)
            batch.append(img_prep_numpy)
            for col in row.keys():
                ret_dict[col].append(row[col])

            if len(batch) >= FLAGS.batch_size:
                batch = np.array(batch).astype(np.float32)
                logging.info("Inferencing batch with shape : %s."%str(batch.shape))
                cats, attrs = model.predict(batch)
                cats, attrs = np.squeeze(cats), np.squeeze(attrs)
                cat = np.squeeze(np.argmax(cats, axis = -1))
                ret_dict['category'].extend(cat.tolist())
                ret_dict['feature'].extend(attrs.tolist())
                batch = []

        if len(batch) > 0:
            batch = np.array(batch).astype(np.float32)
            logging.info("Inferencing batch with shape : %s."%str(batch.shape))
            cats, attrs = model.predict(batch)
            cats, attrs = np.squeeze(cats), np.squeeze(attrs)
            cat = np.squeeze(np.argmax(cats, axis = -1))
            ret_dict['category'].extend(cat.tolist())
            ret_dict['feature'].extend(attrs.tolist())
            batch = []
    
        df_list.append(pd.DataFrame(ret_dict))
        df_final = pd.concat(df_list)
        df_final.to_csv(SAVE_TO_PATH_DICT[FLAGS.dataset])
        logging.info("Saved table with predicted categories and extracted features into %s"%SAVE_TO_PATH_DICT[FLAGS.dataset])

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass