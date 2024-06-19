import socket
from threading import Thread

SERVER_HOST='0.0.0.0'
SERVER_PORT=9001
seperator_token="<SEP>"
#sep is used for separating client name and message

#initialize list/set of all connected client's socket
client_sockets=set()

#for creating a tcp socket
s=socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
#making the port as reusable port

s.bind((SERVER_HOST, SERVER_PORT)) #For binding

s.listen(5) #listen for upcoming connections

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def listen_for_client(cs):
    #This function keeps listening for a message from cs socket
    #Whenever a message is received, broadcast it to all other connected clients

    while True:

        try:
            msg=cs.recv(1024).decode()
        except Exception as e:
            print(f"[!]Error: {e}")
            client_sockets.remove(cs)
        else:
            msg=msg.replace(seperator_token, ": ")
        
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    # for listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket, ))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()