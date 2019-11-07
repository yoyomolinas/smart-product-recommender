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
    python download_images.py --image_dir data/lwaikiki100k_images --meta_path data/meta/lcwaikiki100k.csv --label_path data/labels/lcwaikiki100k_labels.csv
"""

flags.DEFINE_string('image_dir', None, 'download directory')
flags.DEFINE_string('meta_path', None, 'input meta file path')
flags.DEFINE_string('label_path', None, 'output labels file path')
flags.DEFINE_integer('workers', 8, 'number of worker threads')
flags.DEFINE_list('image_size', [300, 400], 'image size in (width, height) format')
flags.mark_flag_as_required('image_dir')
flags.mark_flag_as_required('label_path')
flags.mark_flag_as_required('meta_path')

def fetch_url(inp_queue, out_queue, stop_event):
    while not inp_queue.empty():
        pname, cat_id, cat_name, img_url, prod_url = inp_queue.get()
        try:
            raw_img = urllib.request.urlopen(img_url).read()
            output = (pname, cat_id, cat_name, raw_img, prod_url)
            out_queue.put(output)

        except urllib.error.URLError as e:
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
    prod_names = df.productname.tolist()
    image_urls = df.productimageurl.tolist()
    product_urls = df.producturl.tolist()
    image_paths, cids, cnames, purls, pnames = [], [], [], [], []
    
    # Put into input_queue
    for pname, cat_id, cat_name, img_url, prod_url in zip(prod_names, cat_ids, cat_names, image_urls, product_urls):
        content = (pname, cat_id, cat_name, img_url, prod_url)
        input_queue.put(content)
    
    logging.info("Starting threads.")
    # Create/Start threads
    threads = [threading.Thread(target=fetch_url, args=(input_queue, output_queue, stop_event)) for _ in range(FLAGS.workers)]
    for thread in threads:
        thread.start()


    count = 0
    while True:
        if stop_event.is_set() and output_queue.empty():
            break
        pname, cat_id, cat_name, raw_img, prod_url = output_queue.get()
        image_path = join(FLAGS.image_dir, '%d.jpg' % count)
        # TODO import image to cv2 then resize to FLAGS.image_size 
        with open(image_path,'wb') as f:
            f.write(raw_img)
        image_paths.append(image_path)
        cnames.append(cat_name)
        cids.append(cat_id)
        purls.append(prod_url)
        pnames.append(pname)
        count += 1
        if count % 150 == 0:
            logging.info("Downloaded %i images."%count)

    df_labels = pd.DataFrame({'imagepath' : image_paths, 'labelid' : cids, 'labelname' : cnames, 'producturl' : purls, 'productname' : pnames})
    df_labels.to_csv(FLAGS.label_path)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass