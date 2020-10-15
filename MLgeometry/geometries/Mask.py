"""
Mask Geometry
**Mask is an image (Matrix) that defines which pixel belongs to a class

Parameters:
- mask (ndarray): The parameter mask is a boolean matrix of 2 dimensions
corresponding only to one class
- roi (tuple or list of tuples) boundbox of the region (y1, x1, y2, x2)

MaskRCNN Output:
rois: [N, (y1, x1, y2, x2)] detection bounding boxes
class_ids: [N] int class IDs
scores: [N] float probability scores for the class IDs
masks: [H, W, N] instance binary masks

JCA
Vaico
"""
import reprlib

import numpy as np
import cv2 as cv

from MLgeometry.geometries.Geometry import Geometry


class Mask(Geometry):
    __slots__ = ('idx', 'roi', 'shape', 'keep_mask', 'scale')

    def __init__(self, mask, roi, idx=None, shape=None, keep_mask=False, threshold=0.5, scale=1.0):
        """
        :mask: (ndarray): Boolean matrix of 2 dimensions. If float type. thresholding process is performed
        :roi: (tuple or list of tuples) bound box coordinates (y1, x1, y2, x2)
        :keep_mask: (Bool) Keep original mask in object. If true: store idx and mask
        :threshold: (float) Min value for generating the index mask
        ;scale: (float) mask scaling factor. Values > 0
        """
        self.keep_mask = keep_mask
        self.scale = scale
        if idx is not None and mask is None:
            # When is instantiated from a dict without mask
            if not isinstance(idx[0], int):
                self.idx = [int(i) for i in idx]
            else:
                self.idx = idx
            self.shape = [int(i) for i in shape]
        else:
            # Get only the index of flatten mask (converted into array)
            if isinstance(mask, list):
                mask = np.array(mask, dtype=float)
            if mask.dtype == bool: # Cast boolean masks for resize
                temp_mask = np.zeros(mask.shape)
                temp_mask[mask] = 1
                mask = temp_mask
            if scale != 1 and scale > 0:
                mask = mask.astype(float)
                mask = cv.resize(mask, None, fx=scale,fy=scale)
            # Convert to boolean for generate indexs
            _mask = mask>threshold

            flat = _mask.flatten()
            self.idx = np.where(flat == True)[0].astype(int).tolist()
            self.shape = _mask.shape
            if keep_mask: self.mask = mask # Store original mask

        self.roi = []
        for r in roi:
            if not isinstance(r, list):
                self.roi.append(r.astype(int).tolist())
            else:
                self.roi.append(r)

    def __iter__(self):
        return iter(self.idx)

    def calc_c(self, coords):
        return ((coords[1] + (coords[3] - coords[1])/2,
                coords[0] + (coords[2] - coords[0])/2))

    def centroid(self):
        centers = []
        for r in range(len(self.roi)):
            centers.append(self.calc_c(self.roi[r]))

        return centers

    def _asdict(self):
        d = {
            'shape': self.shape,
            'roi': self.roi,
            'idx': self.idx,
            'scale': self.scale
        }
        if self.keep_mask: 
            d['mask'] = self.mask.tolist()
 
        return d

    def __len__(self):
        return len(self.idx)

    @classmethod
    def _fromdict(cls, info_dict):
        mask = None
        keep_mask = False
        if 'mask' in info_dict: 
            mask = info_dict['mask']
            idx = None
            keep_mask = True
        else:
            idx = info_dict['idx']
            
        return cls(mask,
                   info_dict['roi'],
                   idx=idx,
                   shape=info_dict['shape'],
                   keep_mask=keep_mask,
                   scale=info_dict['scale'] if 'scale' in info_dict else 1
                   )

    def __eq__(self, other):
        return self.idx == other.idx and self.shape == other.shape and self.scale == other.scale

    def __repr__(self):
        class_name = type(self).__name__
        args = {
            'idx': self.idx
        }
        return '{}({})'.format(class_name, reprlib.repr(args))


if __name__ == "__main__":
    import json
    mask = np.random.random((10,10))
    geo = Mask(mask, [], keep_mask=True)
    geo_dict = geo._asdict()
    st = json.dumps(geo_dict)

    new_geo = Mask._fromdict(json.loads(st))
    print(new_geo.mask)
