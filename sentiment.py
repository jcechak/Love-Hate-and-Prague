import json

from twitter_scraper import load_tweets
from sentiment_analysis.main import sentiment


def main():
    # load json
    data = load_tweets('data/tweets.json')
    # annotate
    for i, tweet in enumerate(data):
        print(f'{i} / {len(data)}')
        sent = sentiment(tweet['text'])
        tweet['sentiment'] = sent
    with open('data/tweets_sent.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
