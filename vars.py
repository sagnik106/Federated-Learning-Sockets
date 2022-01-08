from sklearn.linear_model import LinearRegression
import os
import pandas as pd

# Project constants declaration
try:
    CLIENTS_NUM = int(os.environ["FL_CLIENTS"])
except KeyError:
    CLIENTS_NUM = 1
ROUNDS = 500
SERVER_IP = "127.0.0.1"
SERVER_PORT = 40000
CLIENT_BATCH_SIZE = 0.4
CLIENT_SPLIT = 0.6

# Model declaration
def make_model():
    return LinearRegression()

# Dataset initialization
df = pd.read_excel("data/QUES.xlsx", sheet_name="Sheet1")
df = df.append(pd.read_csv("data/UIMS.csv"))
x_g = df[df.columns[1:-1]].to_numpy()
y_g = df[df.columns[-1]].to_numpy()