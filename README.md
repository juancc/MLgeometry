# Geometry
Package for representing data as Objects with common geometries. Used as an interface for prediction elements in Computer Vision problems.
Each predicted object is represented as an Object. Which have geometry, label, score and subobject

Implemented:
- BoundBox
- Point
- Circle
- Polygon

## Importing
For use geometries:
```python
from MLgeometry import Point
P = Point(1,2,z=13)
```
Create from dict:
```python
from MLgeometry import creator
o_dict = {
    'geometry': 'boundbox',
    'label': 'myBB',
    'score': 1,
    'subobject': None
}

new_obj = creator.create_geometry(o_dict)

```
## Methods
Geometry special methods: Geometry._asdict() and Geometry._fromdict(dict)

## License
All rights of this library belongs to Vaico Visión Artificial and no one may distribute, reproduce, or create derivative works.


Vaico