import socket
import numpy as np
from vars import *


soc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
soc.bind((SERVER_IP, SERVER_PORT))

model = make_model()

clients = []
while True:
    msg, _, _, addr = soc.recvmsg(5)
    if addr not in clients:
        clients.append(addr)
    if len(clients) == CLIENTS_NUM:
        break

for round in range(ROUNDS):
    print("ROUND %d"%(round), end='\n')

    # Broadcast
    for c in clients:
        for l in model.get_weights():
            snd = np.reshape(l, (-1,)).tobytes()
            soc.sendto(str.encode(str(len(snd))), c)
            soc.recvmsg(2)
            soc.sendto(snd, c)
            soc.recvmsg(2)

    # Aggregation
    av = [0*i for i in model.get_weights()]
    for c in clients:
        for x in range(len(av)):
            soc.sendto(b"OK", c)
            i, _, _, _=soc.recvmsg(128)
            i = int(i.decode())
            soc.sendto(b"OK", c)
            av[x] = av[x]+np.reshape(np.frombuffer(soc.recvmsg(i)[0], dtype=np.float32), av[x].shape)

    av = [i/CLIENTS_NUM for i in av]
    model.set_weights(av)
    model.evaluate(x_g, y_g)