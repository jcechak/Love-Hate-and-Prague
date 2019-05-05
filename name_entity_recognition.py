from ufal.nametag import *

NER_MODEL_PATH = 'czech-cnec2.0-140304-no_numbers.ner'
NER = Ner.load('/home/jaroslav/Downloads/czech-cnec-140304/czech-cnec2.0-140304-no_numbers.ner')


def get_name_entity(entity, text, tokens):
    return ' '.join([
        text[tokens[i].start: tokens[i].start + tokens[i].length]
        for i in range(entity.start, entity.start + entity.length)
    ])


def find_named_entities(text):
    forms = Forms()
    tokens = TokenRanges()
    entities = NamedEntities()
    tokenizer = NER.newTokenizer()
    tokenizer.setText(text)
    assert tokenizer.nextSentence(forms, tokens)
    NER.recognize(forms, entities)

    entity_types = [entity.type for entity in entities]
    entity_texts = [get_name_entity(entity, text, tokens) for entity in entities]

    return zip(entity_types, entity_texts)


def get_locatable_entities(text):
    return [
        entity_text
        for entity_type, entity_text in find_named_entities(text)
        if entity_type[0] in 'gia'  # g - geo name; i - institution; a - address number (ZIP)
    ]


if __name__ == '__main__':
    import json
    tweets = json.load(open('tweets.json'))
    for tweet in tweets:
        if tweet['coordinates'] is None:
            text = tweet['text']
            print(text)
            print(get_locatable_entities(text))
            input()
