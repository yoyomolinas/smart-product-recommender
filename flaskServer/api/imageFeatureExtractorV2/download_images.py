import os
from os.path import join
import pandas as pd
import numpy as np
import urllib
from queue import Queue
from tqdm import tqdm
from absl import app, flags, logging
from absl.flags import FLAGS
import threading

"""
Example usage:
    python download_images.py --image_dir data/lcwaikiki_images --meta_path data/meta/lcwaikiki.csv --label_path data/labels/lcwaikiki.csv
    python download_images.py --image_dir data/boyner_images --meta_path data/meta/boyner.csv --label_path data/labels/boyner.csv
"""

flags.DEFINE_string('image_dir', None, 'download directory')
flags.DEFINE_string('meta_path', None, 'input meta file path')
flags.DEFINE_string('label_path', None, 'output labels file path')
flags.DEFINE_integer('workers', 8, 'number of worker threads')
flags.mark_flag_as_required('image_dir')
flags.mark_flag_as_required('label_path')
flags.mark_flag_as_required('meta_path')

def fetch_url(inp_queue, out_queue, stop_event):
    while not inp_queue.empty():
        url, attrs = inp_queue.get()
        try:
            raw_img = urllib.request.urlopen(url).read()
            output = (raw_img, attrs)
            out_queue.put(output)

        except Exception as e:
            logging.info("Exception occured %s"%str(e))
            continue
    stop_event.set()

def main(_argv):
    os.makedirs(FLAGS.image_dir, exist_ok=True)
    input_queue = Queue()
    output_queue = Queue()
    stop_event = threading.Event()
    df = pd.read_csv(FLAGS.meta_path)
    cat_names = df.productcategory.tolist()
    unique_cat_names = list(np.unique(cat_names))
    cat_ids = list(map(lambda x: unique_cat_names.index(x), cat_names))
    attributes = {col:df[col].tolist() for col in df.columns}
    num_rows = len(df.index)
    
    # Put into input_queue
    for i in range(num_rows):
        url = attributes['productimageurl'][i]
        attrs = {col:attributes[col][i] for col in attributes.keys()}
        content = (url, attrs)
        input_queue.put(content)
    
    logging.info("Starting threads.")
    # Create/Start threads
    threads = [threading.Thread(target=fetch_url, args=(input_queue, output_queue, stop_event)) for _ in range(FLAGS.workers)]
    for thread in threads:
        thread.start()

    save_dict = {col:[] for col in attrs.keys()}
    save_dict['local_path'] = []
    count = 0
    try:
        while True:
            if stop_event.is_set() and output_queue.empty():
                break
            raw_img, attrs = output_queue.get()
            image_path = join(FLAGS.image_dir, '%d.jpg' % count)
            with open(image_path,'wb') as f:
                f.write(raw_img)
            
            save_dict['local_path'].append(image_path)
            for col in attrs.keys():
                save_dict[col].append(attrs[col]) 
            count += 1
            if count % 150 == 0:
                logging.info("Downloaded %i images."%count)

        df_labels = pd.DataFrame(save_dict)
        df_labels.to_csv(FLAGS.label_path)

        for thread in threads:
            thread.join()
    
    except KeyboardInterrupt:
        df_labels = pd.DataFrame(save_dict)
        df_labels.to_csv(FLAGS.label_path)

        
if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass