import json
import os

import tweepy


def scrape(max_tweets=10000):
    consumer_key = os.environ['API_KEY']
    consumer_secret = os.environ['API_SECRET_KEY']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    places = api.geo_search(query="Prague", granularity="city")
    prague_id = [place
                 for place in places
                 if place.full_name == 'Prague, Czech Republic' and place.place_type == 'city'
                 ][0].id
    max_id = None
    kwargs = {
        'q': 'place:{}'.format(prague_id),
        'lang': 'cs',
        'count': 100
    }
    with open('tweets.json', 'w') as f:
        f.write('[\n')
        tweet_count = 0
        while tweet_count < max_tweets:
            if max_id:
                kwargs['max_id'] = max_id
            new_tweets = api.search(**kwargs)
            if new_tweets:
                print('found {} new tweets!'.format(len(new_tweets)))
                max_id = new_tweets[-1].id
            else:
                print('no new tweets!')
                break
            for tweet in new_tweets:
                f.write(json.dumps(tweet._json, indent=4) + ',\n')
            tweet_count += len(new_tweets)
        f.write(']\n')


def load_tweets(filename='tweets.json'):
    return json.load(open(filename))


