export FL_CLIENTS=10

# Server process
gnome-terminal --command="bash -c 'python3 server.py; $SHELL'"

# Client processes
for((c=1; c<=$FL_CLIENTS; c++))
do
    gnome-terminal --command="bash -c 'python3 client.py; $SHELL'"
done