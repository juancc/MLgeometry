from MLgeometry.geometries.Geometry import Geometry
import numpy as np


class Polyline(Geometry):
    __slots__ = ('all_x', 'all_y')

    def __init__(self, all_x, all_y):
        self.all_x = all_x
        self.all_y = all_y

    def centroid(self):
        pass

    def _asdict(self):
        return {
            'all_x': self.all_x,
            'all_y': self.all_y
        }

    @classmethod
    def _fromdict(cls, info_dict):
        return cls(
            np.array(info_dict['all_x']).astype(float).astype(int),
            np.array(info_dict['all_y']).astype(float).astype(int)
        )

    def __iter__(self):
        return (i for i in (self.all_x, self.all_y))
