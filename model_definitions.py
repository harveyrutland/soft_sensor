import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.regularizers import l1_l2
import numpy as np

def create_model(layers=[64, 32, 16], input_shape=(10,), learning_rate=0.001):
    model = Sequential()
    model.add(Dense(layers[0], activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4), input_shape=input_shape))
    for layer_size in layers[1:]:
        model.add(Dense(layer_size, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4)))
    model.add(Dense(1))
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mean_absolute_error')
    return model

class TerminateOnNaN(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if logs.get('loss') is not None and np.isnan(logs.get('loss')):
            print('NaN loss detected, stopping training')
            self.model.stop_training = True
