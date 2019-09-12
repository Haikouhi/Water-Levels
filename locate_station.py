import requests

from shapely.geometry import mapping, shape
from shapely.prepared import prep
from shapely.geometry import Point

class LocateStation:

    def __init__(self):
        url = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
        self.data = requests.get(url).json()
        self.countries = {}

    def make_dict_coutry(self):
        for feature in self.data['features']:
            geom = feature['geometry']
            country = feature['properties']['ADMIN']
            self.countries[country] = prep(shape(geom))
    
    def get_country(self, lon, lat):

        point = Point(lon, lat)
        for country, geom in self.countries.items():
            if geom.contains(point):
                return country
        
        return 'Unknown'