import re

from unidecode import unidecode


def _preprocess(text):
    # lower
    text = text.lower()
    # split tokens
    text = re.sub(r'\W', ' ', text)
    # shrink white spaces
    text = re.sub(r'\s+', ' ', text)
    # deunicode
    text = unidecode(text)
    return ' ' + text + ' '


def ner_analyze(text):
    """
    Named entity recognition based on streets and points of interest lists.
    Not used in this project so far, because based on the quote from Kuba: "Jiri, to si strc do prdele" it is not good
    enough.
    :param text: to be analyzed for NE
    :return: string with NE's
    """
    # set up lookup string
    lookup_string = []
    # load streets and city districts of Prague
    with open('data/streets.txt', 'r') as f:
        streets = set(f.read().split('\n'))
    # load points of interests from TripAdvisor, mainly hotels and restaurants
    with open('data/pois.txt', 'r') as f:
        pois = set(f.read().split('\n'))
    # preprocess
    text = _preprocess(text)
    # find streets
    for street in streets:
        if ' ' + street + ' ' in text and street not in lookup_string:
            lookup_string.append(street)
            # add number if its around
            idx = text.index(street)
            prev_text = text[:idx].split()
            if prev_text:
                prev_token = prev_text[-1]
                if prev_token.isnumeric():
                    lookup_string.append(prev_token)
            idx = idx + len(street)
            next_text = text[idx:].split()
            if next_text:
                next_token = next_text[0]
                if next_token.isnumeric():
                    lookup_string.append(next_token)
            break
    # find pois
    for poi in pois:
        if poi in text and poi not in lookup_string:
            lookup_string.append(poi)
        break
    return ' '.join(lookup_string)



