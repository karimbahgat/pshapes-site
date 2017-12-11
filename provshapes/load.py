import os
from django.contrib.gis.utils import LayerMapping
from .models import ProvShape

provshape_mapping = {'name': 'Name',
                     'alterns': 'Alterns',
                     'country': 'country',
                     'iso': 'ISO',
                     'fips': 'FIPS',
                     'hasc': 'HASC',
                     'start': 'start',
                     'end': 'end',
                     'geom': 'MULTIPOLYGON',
                     }

path = r"C:\Users\kimok\OneDrive\Documents\GitHub\pshapes\processed.geojson"

def run(verbose=True):
    lm = LayerMapping(ProvShape, "%s"%path, provshape_mapping,
                      transform=False, encoding='utf8')
    lm.save(strict=True, verbose=verbose)

