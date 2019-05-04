import os
import re
import string
import subprocess

from fasttext import fasttext
from nltk.sentiment.util import SAD, HAPPY

from sentiment_analysis.config import *
from sentiment_analysis.czech_stemmer import cz_stem


def load_word_model(model='sentiment_analysis/models/combined_corpora_processed.bin'):
    """
    Loads a fastText word representation model.
    NOTE: Load a word model no more than once per kernel!

    Returns a function for getting word vectors.
    """
    word_model = fasttext.load_model(model)

    def get_word_vector(word):
        """
        Takes a single processed word.

        Returns a list of word vector representation.
        """

        return word_model[word]

    return get_word_vector


def create_processor(aggressive=False):
    '''
    Creates a processor instance with set stemmer aggressivity.
    Default stemmer aggressivity is False, which means 'light' stemming.

    Returns a sentence processor function.
    '''

    punctuation_mapping = str.maketrans(
        dict.fromkeys(string.punctuation + '0123456789²½¾ˇ', ' ')
    )

    happy_emojis_regex = "|".join(map(re.escape, HAPPY))
    sad_emojis_regex = "|".join(map(re.escape, SAD))

    def sent_processor(sentence):
        '''
        Takes a sentence, replaces emojis with keywords, strips off punctuation,
        numbers and excessive whitespace and converts the sentence to lower case.
        The sentence is also capped at `max_sentence_length` words.

        Returns a list of processed words.
        '''

        def split_sentence(sentence):
            split_sentence = re.sub('\s+', ' ', sentence).split(' ')
            return [] if len(sentence) == 0 else split_sentence

        def remove_punc(sentence):
            return \
                re.sub(sad_emojis_regex, ' sadmoji ',
                       re.sub(happy_emojis_regex, ' happymoji ', sentence)
                       ) \
                    .translate(punctuation_mapping) \
                    .lower() \
                    .strip()

        def stem(sentence, aggressive):
            stemmed = [
                          cz_stem(word, aggressive)
                          for word in split_sentence(sentence)
                      ][:max_sentence_length]

            return ['prázdno'] if len(stemmed) < 1 else stemmed

        return stem(remove_punc(sentence), aggressive)

    return sent_processor
