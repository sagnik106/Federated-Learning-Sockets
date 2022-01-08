import socket
import numpy as np
from sklearn.metrics import mean_squared_error
from vars import *

# Server definition
soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
soc.bind((SERVER_IP, SERVER_PORT))
print("[SERVER ONLINE]")
print("IP: ", SERVER_IP, "PORT: ", SERVER_PORT, "\n")

# Server model initialization
model = make_model()
model.coef_ = np.zeros(x_g.shape[1])
model.intercept_ = 0

# Client connection establishment
clients = []
while True:
    msg, _, _, addr = soc.recvmsg(5)
    if addr not in clients:
        clients.append(addr)
    print("[CLIENT CONNECTED] IP : %s, PORT : %d"%addr)
    if len(clients) == CLIENTS_NUM:
        break

for round in range(ROUNDS):
    print("\nROUND %d"%(round), end='\n')

    # Broadcast
    for c in clients:
        snd = np.append(model.coef_, model.intercept_).tobytes()
        soc.sendto(str.encode(str(len(snd))), c)
        soc.recvmsg(2)
        soc.sendto(snd, c)
        soc.recvmsg(2)

    # Aggregation
    av = np.append(model.coef_, model.intercept_)*0
    for c in clients:
        soc.sendto(b"OK", c)
        i, _, _, _=soc.recvmsg(128)
        i = int(i.decode())
        soc.sendto(b"OK", c)
        av = av + np.frombuffer(soc.recvmsg(i)[0], dtype=np.float64)

    av = av/CLIENTS_NUM
    model.coef_ = av[:-1]
    model.intercept_ = av[-1]

    # Server Model Evaluation
    print("Mean Squared Error : ", mean_squared_error(y_g, model.predict(x_g)))