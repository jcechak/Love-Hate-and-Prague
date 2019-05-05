import os

import requests
from googleplaces import GooglePlaces

OSM_URL_TEMPLATE = 'https://nominatim.openstreetmap.org/search?q={}&format=json&polygon=0&addressdetails=1&limit=1&countrycodes=cz&viewbox=13.78235,50.27969,15.15015,49.83887'


def geocoding(text):
    google_api_key = os.environ['GOOGLE_MAPS_API_KEY']
    gmaps = GooglePlaces(google_api_key)
    jsonresult = gmaps.text_search(text + " ,Praha", lat_lng={'lat': 50.075538, 'lng': 14.437800}, radius=50000)
    if len(jsonresult.places) == 0:
        return None
    jsonresult.places.reverse()
    place = jsonresult.places.pop()
    lat = place.geo_location.get('lat')
    lng = place.geo_location.get('lng')
    return {'lat': float(lat), 'lng': float(lng)}


def geocoding_osm(text):
    response = requests.get(OSM_URL_TEMPLATE.format(text.replace(' ', '+'))).json()
    return {'lat': float(response[0]['lat']), 'lon': float(response[0]['lon'])}
