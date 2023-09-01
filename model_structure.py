# my_model.py
import tensorflow as tf

def create_my_model(state_size, action_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(20, activation='relu', input_shape=(state_size + action_size,)),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(action_size)
    ])
    return model
