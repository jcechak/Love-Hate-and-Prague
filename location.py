from googleplaces import GooglePlaces
import os


def get_location(text):
    google_api_key = os.environ['GOOGLE_MAPS_API_KEY']
    gmaps = GooglePlaces(google_api_key);
    jsonresult = gmaps.text_search(text + " ,Praha", lat_lng= {'lat':50.075538, 'lng':14.437800}, radius=50000)
    for item in jsonresult.places:
        print(item)
    return jsonresult.places

