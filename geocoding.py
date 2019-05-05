from googleplaces import GooglePlaces
import os


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
