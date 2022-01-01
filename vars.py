from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.datasets import load_iris
from sklearn.preprocessing import OneHotEncoder
import pickle
import numpy as np

# Project constants declaration
CLIENTS_NUM = 1
ROUNDS = 5
SERVER_IP = "127.0.0.1"
SERVER_PORT = 30000

# Model declaration
def make_model():
    model = Sequential()
    model.add(Dense(16, input_shape=(4,), activation='relu'))
    model.add(Dense(3, activation='softmax'))
    model.compile(Adam(), "categorical_crossentropy", ["accuracy"])
    return model

# Dataset initialization
x, y = load_iris(return_X_y=True)
ohe = OneHotEncoder(sparse=False)
y = ohe.fit_transform(np.reshape(y, (-1, 1)))

with open("instances/ohe.pkl", "wb") as f:
    pickle.dump(ohe, f)