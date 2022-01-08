import socket
import numpy as np
from sklearn.metrics import mean_squared_error
from vars import *

server_address = (SERVER_IP, SERVER_PORT)

model = make_model()
idx = np.random.randint(0, y_g.shape[0], round(CLIENT_SPLIT*y_g.shape[0]))
x = x_g[idx, :]
y = y_g[idx]

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
print("[CLIENT ONLINE]")
client.sendto(b"Hello", server_address)
print("IP : ", client.getsockname()[0], ", PORT : ", client.getsockname()[1])

for rnd in range(ROUNDS):
    print("\nROUND %d"%(rnd), end='\n')
    # Server Model weights
    i = client.recvmsg(128)[0]
    i = int(i.decode())
    client.sendto(b"OK", server_address)
    ws = np.frombuffer(client.recvmsg(i)[0], dtype=np.float32)
    client.sendto(b"OK", server_address)

    model.coef_ = ws[:-1]
    model.intercept_ = ws[-1]

    #client training
    sub_idx = np.random.randint(0, y.shape[0], round(CLIENT_BATCH_SIZE*y.shape[0]))
    model.fit(x[sub_idx, :], y[sub_idx])
    print("Mean Squared Error : ", mean_squared_error(y, model.predict(x)))

    #client weight aggregation phase
    client.recvmsg(2)
    snd = np.append(model.coef_, model.intercept_).tobytes()
    client.sendto(str.encode(str(len(snd))), server_address)
    client.recvmsg(2)
    client.sendto(snd, server_address)