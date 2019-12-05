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
    python extract.py --dataset boyner --save_to data/features/boyner.csv --model models/bigx_act.hdf5 --batch_size 100 --input_size 256,256
"""

DEFAULT_BATCH_SIZE = 1000
DEFAULT_IMAGE_SIZE = [256, 256]
DATASET_PATH_DICT = {
    'boyner':['data/labels/boyner.csv'],
    'lcwaikiki':['data/labels/lcwaikiki.csv'],
    'all': ['data/labels/boyner.csv', 'data/labels/lcwaikiki.csv']}

flags.DEFINE_integer('batch_size', DEFAULT_BATCH_SIZE, 'batch size should not be too large as to exceed RAM capacity, dont use if in doubt')
flags.DEFINE_string('dataset', None, 'should be one of %s'%str(list(DATASET_PATH_DICT.keys())))
flags.DEFINE_string('model', None, "path to model")
flags.DEFINE_string('save_to', None, "put any path here, recommendded is : data/features/x.csv")
flags.DEFINE_list('input_size', DEFAULT_IMAGE_SIZE, 'input size in (width, height) format')

flags.mark_flag_as_required('dataset')
flags.mark_flag_as_required('model')
flags.mark_flag_as_required('save_to')

def main(_):
    assert FLAGS.dataset in DATASET_PATH_DICT.keys(), 'dataset should be one of %s'%str(list(DATASET_PATH_DICT.keys()))
    input_size = (int(FLAGS.input_size[0]) , int(FLAGS.input_size[1])) # (width, height)
    df_list = []
    logging.info("Extracting features for : %s"%FLAGS.dataset)
    for dataset_path in DATASET_PATH_DICT[FLAGS.dataset]:
        logging.info("Extracting features from path : %s"%dataset_path)
        df = pd.read_csv(dataset_path)
        new_cols = {'category':[], 'feature':[]} # columns to be appended to data frame when the program ends
        batch = []
        model = keras.models.load_model(FLAGS.model)
        assert len(model.outputs) == 2, "model should have two outputs which are categories and features respectively"
        for i, row in tqdm(df.iterrows()):
            img = Image.open(row['local_path'])
            img_prep = utils.preprocess(img, size = input_size)
            batch.append(np.array(img_prep))
            if len(batch) >= FLAGS.batch_size:
                batch = np.array(batch).astype(np.float32)
                cats, attrs = model.predict(batch)
                cats, attrs = np.squeeze(cats), np.squeeze(attrs)
                cat = np.argmax(cats)
                new_cols['category'].append(int(cat))
                new_cols['feature'].append(attrs.tolist())
                batch = []
                break

        # for colname, colvals in new_cols.items():
        #     df[colname] = colvals        
        
        df_list.append(df)

    df_final = pd.concat(df_list)
    print(df_final)
    df_final.to_csv(FLAGS.save_to)
    logging.info("Saved table with predicted categories and extracted features into %s"%FLAGS.save_to)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass