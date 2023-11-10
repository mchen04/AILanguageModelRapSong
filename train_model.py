import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import ReduceLROnPlateau
import matplotlib.pyplot as plt

def plot_training_metrics(history, metric_name):
    plt.plot(history.history[metric_name])
    plt.xlabel("Epochs")
    plt.ylabel(metric_name.capitalize())
    plt.title(f"Training {metric_name.capitalize()}")
    plt.show()

def tokenize_corpus(corpus):
    tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True, split=' ', oov_token="<OOV>")  # Preserve '\n'
    tokenizer.fit_on_texts(corpus)
    
    sequences = []
    for song in corpus:
        token_list = tokenizer.texts_to_sequences([song])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            sequences.append(n_gram_sequence)

    return tokenizer, sequences

def build_and_train_model(corpus, batch_size=512):
    tokenizer, song_sequences = tokenize_corpus(corpus)
    vocab_size = len(tokenizer.word_index) + 1

    if not song_sequences:
        print("No sequences generated. Check the tokenizer and the input data.")
        return None, None

    max_sequence_length = max([len(seq) for seq in song_sequences])
    song_sequences = np.array(pad_sequences(song_sequences, maxlen=max_sequence_length, padding='pre'))

    X, labels = song_sequences[:,:-1], song_sequences[:,-1]
    Y = tf.keras.utils.to_categorical(labels, num_classes=vocab_size)

    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, 200, input_length=max_sequence_length - 1),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(150, return_sequences=True, recurrent_regularizer='l2')), 
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(100, recurrent_regularizer='l2')),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(vocab_size, activation='softmax')
    ])

    adam_optimizer = tf.keras.optimizers.legacy.Adam(learning_rate=0.005, clipvalue=1.0)
    model.compile(optimizer=adam_optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1, min_lr=0.00001)

    training_history = model.fit(X, Y, epochs=100, verbose=1, batch_size=batch_size, validation_split=0.2, callbacks=[lr_scheduler])

    plot_training_metrics(training_history, 'accuracy')
    plot_training_metrics(training_history, 'loss')

    model.save('lyrics_model.keras', save_format='tf')

    return model, tokenizer

if __name__ == '__main__':
    lyrics_data = open('lyrics.txt').read().lower().splitlines()  # Keep newlines as it is
    build_and_train_model(lyrics_data)