import unittest
import json

import numpy as np
import cv2 as cv

from MLgeometry.geometries.Mask import Mask

class MaskTests(unittest.TestCase):
    def test_serialize_with_mask(self):
        mask = np.random.random((10,10))
        geo = Mask(mask, [], keep_mask=True)
        geo_dict = geo._asdict()
        st = json.dumps(geo_dict)

        new_geo = Mask._fromdict(json.loads(st))
        self.assertTrue(np.equal(mask, new_geo.mask).all())

    def test_scale_mask(self):
        mask = np.random.random((100,100))
        geo = Mask(mask, [], keep_mask=True, scale=0.5)
        geo_dict = geo._asdict()

        mask_scaled = cv.resize(mask, None, fx=0.5,fy=0.5)

        self.assertTrue(np.equal(mask_scaled, geo_dict['mask']).all())
    
    def test_bool_mask(self):
        mask_init = np.random.random((20,20)) > 0.5
        mask = np.zeros((20,20))
        mask[mask_init] = 1

        mask_scaled = cv.resize(mask, None, fx=0.5,fy=0.5)
        mask_bool = mask_scaled > 0.5
        flat = mask_bool.flatten()
        indexs = np.where(flat == True)[0].astype(int).tolist()

        geo = Mask(mask, [], keep_mask=True, scale=0.5)

        self.assertEquals(geo.idx, indexs)



if __name__ == '__main__':
    unittest.main()