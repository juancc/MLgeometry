"""
Line Geometry Class
Line defined with two points. Point could be any iterable.

SUPPORT
 - len
 - equals

JCA
Vaico
"""

from MLgeometry.geometries.Geometry import Geometry

class Line(Geometry):
    __slots__ = ('p1', 'p2')
    def __init__(self, p1, p2):
        self.p1 = tuple(p1)
        self.p2 = tuple(p2)

    def centroid(self):
       return ( (self.p1[0] + self.p2[0])/2, (self.p1[1] + self.p2[1])/2  )

    def _asdict(self):
        return {
            'p1': self.p1,
            'p2': self.p2
        }

    @classmethod
    def _fromdict(cls, info_dict):
        return cls(
            info_dict['p1'],
            info_dict['p2']
        )

    def __iter__(self):
        return (i for i in [self.p1, self.p2])




if __name__ == "__main__":
    l = Line((1,3), (3,4))
    print(l.centroid())
    for p in l:
        print(p)