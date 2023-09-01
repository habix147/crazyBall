import math
import random
import config
import tensorflow
import tensorflow as tf
import numpy as np
import os
import datetime
from model_structure import create_my_model


# Design the RL Agent
class RLAgent:
    def __init__(self, state_size, action_size, x_min, x_max, discount_factor,  buffer_size):
        self.state_size = state_size
        self.action_size = action_size
        self.x_min = x_min
        self.x_max = x_max
        self.model = self.build_model()

    def build_model(self):
        model = create_my_model(self.state_size, self.action_size)
        optimizer = tf.keras.optimizers.Adam()
        model.compile(optimizer=optimizer, loss='mse')
        return model

    def get_action(self, circle_x, circle_y, control_line_y):
        threshold = 0.05
        random_number = random.random()  # Generate a random number between 0 and 1
        action_values = np.arange(self.x_min, self.x_max + 1)
        if random_number > threshold:
            num_actions = self.x_max - self.x_min + 1
            state = np.array([[circle_x, circle_y, control_line_y, 0]])
            # Create a state-action matrix with all possible actions
            state_plus_actions = np.tile(state, (num_actions, 1))
            state_plus_actions[:, -1] = action_values
            # Predict Q-values for all state-action pairs in parallel
            q_values = self.model.predict(state_plus_actions, verbose= -1)
            # Find the action corresponding to the minimum Q-value
            action = action_values[np.argmax(q_values)]
            # print(np.max(q_values))
        else:
            action = random.choice(action_values)
        return action


    def load_backup_model(self, filepath):
        # Load the model weights from the file
        self.model.load_weights(filepath)







