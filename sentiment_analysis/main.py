import os
import sys
import warnings

from sentiment_analysis.model import CNN

model = CNN('combined')
model.load()

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    warnings.filterwarnings("ignore")


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stdout__
    warnings.simplefilter('module')


def sentiment(text):
    """
    Analyse text in Czech language for sentiment.
    :param text: text to be analyzed
    :return: NEG, NEU or POS
    """
    blockPrint()
    result = model.predict(text)
    enablePrint()
    if result == 0:
        return 'NEG'
    elif result == 1:
        return 'NEU'
    elif result == 2:
        return 'POS'
    raise ValueError()
