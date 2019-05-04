from keras.layers import Conv1D, MaxPooling1D, GlobalMaxPooling1D, Dense
from keras.models import Sequential
import numpy as np

from sentiment_analysis.utils import *
from sentiment_analysis.config import *

word_vector = load_word_model()
# Create a processor instance
sent_processor = create_processor()


def sentence_tensor(sentence):
    """
    Takes a sentence, runs it through the sentence processor
    and obtains word vectors for all of the processed words.
    Pads the array so it matches our input size.

    Returns a 2D numpy array containing word vectors.
    """

    sentence_array = [word_vector(word) for word in sent_processor(sentence)]

    return np.pad(sentence_array,
                  pad_width=(
                      (0, max_sentence_length - len(sentence_array)),
                      (0, 0)
                  ),
                  mode='constant')


class CNN:
    def __init__(self, name='unnamed', optimizer='adagrad'):
        """
        Creates and compiles a new model. Prints out its summary.
        """

        self.name = name
        self.model_weights = 'sentiment_analysis/models/weights.best.{}.hdf5'.format(self.name)

        self.model = Sequential()
        self.model.add(
            Conv1D(filters=64, kernel_size=4,
                   activation='relu', padding='same',
                   input_shape=(max_sentence_length, word_vector_dim))
        )
        self.model.add(MaxPooling1D(pool_size=2))

        self.model.add(
            Conv1D(filters=128, kernel_size=8,
                   activation='relu', padding='same', )
        )
        self.model.add(MaxPooling1D(pool_size=2))

        self.model.add(GlobalMaxPooling1D())
        self.model.add(Dense(units=len(target_labels), activation='softmax'))

        self.model.compile(optimizer=optimizer,
                           loss='categorical_crossentropy',
                           metrics=['categorical_accuracy'])
        self.model.summary()

    def load(self):
        """
        Loads the saved weights for the model.

        Returns self.
        """

        self.model.load_weights(self.model_weights)
        # print('_' * 65 + '\nLoaded the weights for \'{}\' model.\n'.format(self.name))

        return self

    def predict(self, sentence, proba=False):
        """
        Takes a `sentence` and predicts its label.

        Returns the label index.
        """

        sentence_array = np.expand_dims(sentence_tensor(sentence), axis=0) \
            if type(sentence) is str else \
            np.expand_dims(sentence, axis=0)

        prediction = self.model.predict(sentence_array)
        return np.argmax(prediction) if proba is False else prediction

    def predict_proba(self, sentence):
        """
        Takes a `sentence` and predicts its label.

        Returns a vector containing probabilities of belonging to each of the labels.
        """

        return self.predict(sentence, True)
