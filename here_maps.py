import json
import os

import flatzone_scraper
import twitter_scraper


def make_geotweet(tweet):
    if tweet["coordinates"] is None:
        tweet["coordinates"] = {'type': 'Point', 'coordinates': [14.0, 50.0]}  # 50.07062,14.45615

    return {
        "type": "Feature",
        "geometry": tweet["coordinates"],
        "properties": {
            "text": '"' + tweet['text'] + '"',
            "sentiment": 0
        }
    }


def prepare_twitter_geojson():
    tweets = twitter_scraper.load_tweets()
    geo_tweets = [make_geotweet(tweet) for tweet in tweets]
    geo_json = {
        "type": "FeatureCollection",
        "features": geo_tweets
    }
    json.dump(geo_json, open('twitter_geodata.json', 'w'), indent=4)


def make_geosestate(estate):
    return {
        "type": "Feature",
        "geometry": {
            'type': 'Point',
            'coordinates': [
                estate['gps']['lon'],
                estate['gps']['lat']
            ]
        },
        "properties": estate
    }


def prepare_flatzone_geojson():
    flatzone_data = flatzone_scraper.download_flatzone()
    geo_estates = [make_geosestate(estate) for estate in flatzone_data['data']['searchByDistance']['estates']]
    geo_json = {
        "type": "FeatureCollection",
        "features": geo_estates
    }
    json.dump(geo_json, open('flatzone_geodata.json', 'w'), indent=4)


def load_geodata():
    prepare_twitter_geojson()
    prepare_flatzone_geojson()
    os.system("sh load_geodata.sh")
