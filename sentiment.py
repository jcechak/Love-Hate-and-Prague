import pandas as pd
import numpy as np
import json
import requests

from twitter_scraper import load_tweets
from sentiment_analysis.main import sentiment
from sentiment_analysis.czech_stemmer import cz_stem


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


class SentimentAnalyzer(object):
    def __init__(self):
        with open('sentiment_stem_list.txt', 'r') as f:
            lines = f.readlines()
        stem_list = [line.strip().split('\t') for line in lines]
        self.stem_dict = {stem: int(score) for stem, score in stem_list}

    def analyze_text(self, text):
        words = text.split()
        stems = [cz_stem(word) for word in words]
        return int(np.clip(sum(self.stem_dict.get(stem, 0) for stem in stems), a_min=-1, a_max=1))


def analyze_sentiments_2():
    analyzer = SentimentAnalyzer()
    tweets = json.load(open('tweets.json'))

    for tweet in tweets:
        tweet['sentiment2'] = analyzer.analyze_text(tweet['text'])

    # differences = [(tweet['sentiment'], tweet['sentiment2']) for tweet in tweets]

    # df = pd.DataFrame(differences, columns=('N', 'W'))
    # pd.crosstab(df.N, df.W)

    json.dump(tweets, open('tweets.json', 'w'), indent=4)


def analyze_sentiment_3():
    tweets = json.load(open('tweets.json'))
    for tweet in tweets:
        response = requests.post('https://demo.geneea.com/interpretDoc', data={
            "text": "{}".format(tweet['text']),
            "language": 'cs', "domain": "news", "refDate": "NOW"})
        tweet['sentiment3'] = json.loads(response.json())['sentiment']['polarity']

    json.dump(tweets, open('tweets.json', 'w'), indent=4)


def rescale_and_sum_sentiment():
    tweets = json.load(open('tweets.json'))
    sentiments = pd.Series([tweet['sentiment3'] for tweet in tweets])
    sentiments = sentiments / max(abs(sentiments))

    for tweet, sentiment in zip(tweets, sentiments):
        tweet['sentiment_sum'] = tweet['sentiment'] + tweet['sentiment2'] + sentiment

    json.dump(tweets, open('tweets.json', 'w'), indent=4)


if __name__ == '__main__':
    main()
