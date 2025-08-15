import numpy as np
import random

class Agent():
    def __init__(self):
        self.learning_rate = 0.01
        self.epsilon = 1.0
        self.epsilon_decay = 0.001
        self.final_epsilon = 0.001
        self.discount_factor = 0.95
        self.q_values = np.zeros((2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4))

        # Track learning progress
        self.training_error = []
        self.no_food_steps = 0

    # epsilon-greedy policy
    def get_action(self, state):
        # exploration
        if random.random() < self.epsilon:
            return random.choice([0, 1, 2, 3])
        # exploitation
        return np.argmax(self.q_values[state])
    
    # update rule
    def update(self, state, action, reward, next_state):
        target = reward + self.discount_factor * np.max(self.q_values[next_state])
        error = target - self.q_values[state][action]
        self.q_values[state][action] = self.q_values[state][action] + self.learning_rate * error

        self.training_error.append(error)

    def decay_epsilon(self):
        # reduce epsilon (reduce exploration) (increase exploitation)
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)

    def stop_exploration(self):
        self.epsilon = 0