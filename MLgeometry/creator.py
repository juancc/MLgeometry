"""
Create Objects from dictionaries

JCA
Vaico
"""

# from inspect import signature

from MLgeometry import geometries
from MLgeometry.Object import Object

def from_dict(d):
    """Create geometry from dict"""
    new_obj = None
    if d:
        if isinstance(d, list):
            new_obj = []
            for obj in d:
                new_obj.append(from_dict(obj))
        else:
            new_obj = Object(
                    geometry = create_geometry(d),
                    label = d['label'] if 'label' in d else None,
                    score = d['score'] if 'score' in d else None,
                    subobject = from_dict(d['subobject'])  if 'subobject' in d else None
                )
    return new_obj

def create_geometry(info):
    """Create geometry from dict"""
    if info:
        for geo in dir(geometries):
            if geo.lower() in info:
                cls = getattr(geometries, geo)
                new_geom = cls._fromdict(info[geo.lower()])
                return new_geom
    return None # Classification does not have geometry

