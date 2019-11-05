import os
from os.path import join
import pandas as pd
import numpy as np
import urllib
from tqdm import tqdm
from absl import app, flags, logging
from absl.flags import FLAGS

flags.DEFINE_string('image_dir', None, 'download directory')
flags.DEFINE_string('meta_path', None, 'input meta file path')
flags.DEFINE_string('label_path', None, 'output labels file path')
flags.mark_flag_as_required('image_dir')
flags.mark_flag_as_required('label_path')
flags.mark_flag_as_required('meta_path')

def main(_argv):
    df = pd.read_csv(FLAGS.meta_path)
    cat_names = df.productcategory.tolist()
    unique_cat_names = list(np.unique(cat_names))
    cat_ids = list(map(lambda x: unique_cat_names.index(x), cat_names))
    urls = df.productimageurl.tolist()
    image_paths, cids, cnames = [], [], []
    for i, (cat_name, cat_id, url) in tqdm(enumerate(zip(cat_names, cat_ids, urls))):
        image_path = join(FLAGS.image_dir, '%d.jpg' % i)
        # Continue fetching despite previous fail
        if os.path.isfile(image_path):
            continue
        try:
            content = urllib.request.urlopen(url)
            with open(image_path,'wb') as f:
                f.write(content.read())
            image_paths.append(image_path)
            cnames.append(cat_name)
            cids.append(cat_id)

        except urllib.error.URLError as e:
            pass
    
    df_labels = pd.DataFrame({'path' : image_paths, 'label_id' : cids, 'label_name' : cnames})
    df_labels.to_csv(FLAGS.label_path)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass