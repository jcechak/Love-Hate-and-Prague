import json

from geocoding import geocoding


def main():
    """
    Enhance data with geo coordinates using geocoding.
    """
    with open('data/tweets_sent.json', 'r') as f:
        data = json.load(f)
    for i, tweet in enumerate(data):
        print(f'{i} / {len(data)}')
        # geocoding
        coord = geocoding(tweet['text'])
        if coord:
            tweet['coordinates'] = {
                'type': 'Point',
                'coordinates': [
                    coord['lng'],
                    coord['lat']
                ]
            }
    # filter only with coordinates
    data = [tweet for tweet in data if tweet['coordinates'] is not None]
    print('Size: ', len(data))
    with open('data/tweets_complete.json', 'w') as f:
        json.dump(data, f, sort_keys=True, indent=True)


if __name__ == '__main__':
    main()