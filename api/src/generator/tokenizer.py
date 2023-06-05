import tensorflow as tf


def tokenizer(path_to_file):

    text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

    vocab = sorted(set(text))

    ids_from_chars = tf.keras.layers.StringLookup(
        vocabulary=list(vocab), mask_token=None)

    chars_from_ids = tf.keras.layers.StringLookup(
        vocabulary=ids_from_chars.get_vocabulary(), invert=True, mask_token=None)

    return (ids_from_chars, chars_from_ids)
