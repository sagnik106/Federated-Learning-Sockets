export FL_CLIENTS=10
echo $FL_CLIENTS

gnome-terminal --command="bash -c 'python3 server.py; $SHELL'"

for((c=1; c<=$FL_CLIENTS; c++))
do
    echo "hello $i"
    gnome-terminal --command="bash -c 'python3 client.py; $SHELL'"
done