import tensorflow as tf


def restore_model(model_path):
    model = tf.saved_model.load(model_path)
    return model
