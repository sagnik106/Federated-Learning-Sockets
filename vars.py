from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

CLIENTS_NUM = 1
ROUNDS = 5
SERVER_IP = "127.0.0.1"
SERVER_PORT = 30000

def make_model():
    model = Sequential()
    model.add(Dense(16, input_shape=(4,)))
    model.add(Dense(1, activation='sigmoid'))
    return model