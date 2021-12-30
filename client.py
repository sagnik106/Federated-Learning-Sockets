import socket
import numpy as np
from vars import *

server_address = (SERVER_IP, SERVER_PORT)

model = make_model()

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
client.sendto(b"Hello", server_address)

for round in range(ROUNDS):
    print("ROUND %d"%(round), end='\n')
    # Server Model weights
    g = list()
    for l in model.get_weights():
        i, _, _, _ = client.recvmsg(128)
        i = int(i.decode())
        client.sendto(b"OK", server_address)
        g.append(np.reshape(np.frombuffer(client.recvmsg(i)[0], dtype=np.float32), l.shape))
        client.sendto(b"OK", server_address)

    model.set_weights(g)

    #client training

    #client aggregation phase
    for l in model.get_weights():
        client.recvmsg(2)
        snd = np.reshape(l, (-1,)).tobytes()
        client.sendto(str.encode(str(len(snd))), server_address)
        client.recvmsg(2)
        client.sendto(snd, server_address)