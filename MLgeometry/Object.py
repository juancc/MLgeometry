"""
Prediction Objects tha is returned by models.
Attributes:
    - geometry: Instance of a class that implements MLgeometry.geometry bastract class
    - label: Object name
    - score: confidence of the prediction
    - subobject: list of child Objects
    - properties: dictionary of extra attributes of the object: weight, distance, color...

JCA
Vaico
"""
from MLgeometry import geometries


class Object():
    __slots__ = ('geometry', 'label', 'score', 'subobject', 'properties')

    def __init__(self, geometry=None, label=None, score=None, subobject=None, properties=None):
        self.geometry = geometry
        self.label = label
        self.score = score
        self.subobject = subobject
        self.properties = properties

    def values(self):
        """Return tuple of object values"""
        return (self.geometry,self.label,self.score, self.subobject,self.properties)

    def __eq__(self, other):
        return other.values() == self.values()

    def __repr__(self):
        class_name = type(self).__name__
        args_rep = str({i: getattr(self,i) for i in self.__slots__ })[1:-1]
        rep = '{}({})'.format(class_name, args_rep)
        return rep

    def _asdict(self):
        d = {
            'label': self.label,
            'score': float(self.score) if self.score else None,
        }
        if self.properties: d['properties'] = self.properties

        if self.geometry:
            d[str(type(self.geometry).__name__).lower()] = self.geometry._asdict()

        if self.subobject:
            if isinstance(self.subobject, list):
                d['subobject'] = [subobj._asdict() for subobj in self.subobject]
            else:
                d['subobject'] = [self.subobject._asdict()]

        return d

    @classmethod
    def from_dict(cls, d):
        """Create geometry from dict"""
        new_obj = None
        if d:
            if isinstance(d, list):
                new_obj = []
                for obj in d:
                    new_obj.append(Object.from_dict(obj))
            else:
                new_obj = cls(
                        geometry = Object.create_geometry(d),
                        label = d['label'] if 'label' in d else None,
                        score = d['score'] if 'score' in d else None,
                        properties = d['properties'] if 'properties' in d else None,
                        subobject = Object.from_dict(d['subobject'])  if 'subobject' in d else None
                    )
        return new_obj

    @classmethod
    def create_geometry(cls, info):
        """Create geometry from dict"""
        if info:
            for geo in dir(geometries):
                if geo.lower() in info:
                    cls = getattr(geometries, geo)
                    new_geom = cls._fromdict(info[geo.lower()])
                    return new_geom
        return None # Classification does not have geometry