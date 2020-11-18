import unittest
from os.path import join
import pickle
import copy
import numpy as np
import batchgen
import utils



class TestBatchGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dt = utils.DirectoryTree("data/Category and Attribute Prediction Benchmark/")
        print("Loading data..")
        with open(join(cls.dt.Anno.path, 'meta.pickle'), 'rb' ) as f:
            cls.data = pickle.load(f)

    def test_getitem(self):
        print("testing getitem")
        args_dict_1 = dict(
            image_paths = list(map(lambda path: join(self.dt.Img.path, path), self.data['img_names'])), 
            bboxes = self.data['bbox_coords'],
            categories=self.data['cat_labels'],
            attributes=self.data['attr_labels'],
            eval_status=self.data['eval_status'],
            batch_size=32,
            image_size=(156, 156),
            shuffle = True,
            jitter = False,
            crop = False,
            mode = 'train'
        )
        gen1 = batchgen.BatchGenerator(**args_dict_1)
        gen2 = batchgen.BatchGenerator(**args_dict_1)
        batch1 = gen1.__getitem__(0)
        batch2 = gen2.__getitem__(0)
        batch3 = gen1.__getitem__(90)
        batch4 = gen1.__getitem__(1)
        self.assertEqual(batch1[0].shape, (32, 156, 156, 3))
        self.assertTrue(np.all(batch1[0] == batch2[0]))
        self.assertFalse(np.all(batch1[0] == batch3[0]))
        self.assertFalse(np.all(batch3[0] == batch4[0]))
        self.assertTrue(np.all(gen1.index == gen2.index))
        index_prev = gen1.index.copy()
        gen1.on_epoch_end()
        index_next = gen1.index.copy()
        self.assertFalse(np.all(index_prev == index_next))
        

    
    def test_jitter(self):
        print("testing augmentation")
        args_dict = dict(
            image_paths = list(map(lambda path: join(self.dt.Img.path, path), self.data['img_names'])), 
            bboxes = self.data['bbox_coords'],
            categories=self.data['cat_labels'],
            attributes=self.data['attr_labels'],
            eval_status=self.data['eval_status'],
            batch_size=32,
            image_size=(156, 156),
            shuffle = True,
            jitter = True,
            crop = False,
            mode = 'train'
        )
        gen = batchgen.BatchGenerator(**args_dict)
        X1, _ = gen.__getitem__(1)
        X2, _ = gen.__getitem__(1)
        self.assertFalse(np.all(X1 == X2))

        args_dict['jitter'] = False
        gen = batchgen.BatchGenerator(**args_dict)
        X1, _ = gen.__getitem__(1)
        X2, _ = gen.__getitem__(1)
        self.assertTrue(np.all(X1 == X2))
    
    def test_mode(self):
        print("testing mode")
        train_args_dict = dict(
            image_paths = list(map(lambda path: join(self.dt.Img.path, path), self.data['img_names'])), 
            bboxes = self.data['bbox_coords'],
            categories=self.data['cat_labels'],
            attributes=self.data['attr_labels'],
            eval_status=self.data['eval_status'],
            batch_size=32,
            image_size=(156, 156),
            shuffle = True,
            jitter = True,
            crop = False,
            mode = 'train'
        )
        test_args_dict = dict(
            image_paths = list(map(lambda path: join(self.dt.Img.path, path), self.data['img_names'])), 
            bboxes = self.data['bbox_coords'],
            categories=self.data['cat_labels'],
            attributes=self.data['attr_labels'],
            eval_status=self.data['eval_status'],
            batch_size=32,
            image_size=(156, 156),
            shuffle = True,
            jitter = True,
            crop = False,
            mode = 'test'
        )
        gen_train = batchgen.BatchGenerator(**train_args_dict)
        gen_test = batchgen.BatchGenerator(**test_args_dict)
        self.assertGreater(len(gen_train.index), len(gen_test.index))

if __name__ == '__main__':
    unittest.main()

