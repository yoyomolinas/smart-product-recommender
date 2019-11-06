from PIL import Image
from absl import app, flags, logging
from absl.flags import FLAGS

"""
This script, given a deployed model, a directory of images, and a path to save features, 
extracts features from each image and saves into the specified path in csv (or whatever) format.

Example usage: 
    python extract.py --model_path deploy/test_minix_model.hdf5 --save_path data/features/test_minix_features.csv --input_size 300,400
"""

DEFAULT_IMAGE_SIZE = (300, 400) # width, height

flags.DEFINE_string('model_path', None, 'keras saved model path')
flags.DEFINE_string('save_path', None, 'path to save features - should be in data/features/something ')
flags.DEFINE_list('input_size', DEFAULT_IMAGE_SIZE, 'input size in (width, height) format')
flags.mark_flag_as_required('model_path')
flags.mark_flag_as_required('save_path')

def main(_argv):
    input_size = (int(FLAGS.input_size[0]) , int(FLAGS.input_size[1])) # (width, height)
    # TODO Using PIL open each and every image and resize into input_size (defined above)
    # TODO Load specified model in FLAGS.model_path using keras.models.load_model(FLAGS.model_path) 
    # TODO Execute forward pass for every image and put output features into pandas dataframe storing
    # absolute image path, and catgeory alongside features.
    # TODO save data frame into FLAGS.save_path (in csv?)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass

