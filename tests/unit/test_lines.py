import unittest

from MLgeometry.geometries import Line


class PointTests(unittest.TestCase):

    def test_line_centroid(self):
        l = Line((1,3), (3,4))
        self.assertEqual(l.centroid(), (2.0, 3.5))

    def test_line_as_dict(self):
        l = Line((1,3), (3,4))
        self.assertEqual(l._asdict(), {'p1': (1,3), 'p2': (3,4)})

    def test_line_from_dict(self):
        d = {'p1': (0,0), 'p2': (1,1)}
        l = Line._fromdict(d)
        self.assertEqual(l, Line((0,0), (1,1)))




if __name__ == '__main__':
    unittest.main()
