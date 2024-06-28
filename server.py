import socket
import threading

HOST='127.0.0.1'
PORT=4109
LISTENER_LIMIT=5
active_clients= [] #list of all currently connected user

#Function for listen upcoming messages from a client
def listen_for_messages(client, username):

    while 1:

        message=client.recv(2048).decode('utf-8')

        if message!= '':
            final_msg=username+ '~'+ message
            send_messages_to_all(message=final_msg)
        else:
            print(f"The message sent from client {username} is empty")

#Function to send message to a single client
def send_message_to_client(client,message):
    
    client.sendall(message.encode())
def send_messages_to_all(message):

    for user in active_clients:

        send_message_to_client(user[1], message)

def client_handler(client):
    while True:
        username=client.recv(2048).decode('utf-8')

        if username!= '' :
            active_clients.append((username,client))
            prompt_message = "Server~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")
        
    threading.Thread(target=listen_for_messages, args=(client, username,)).start()

    


def main():
    #Creating the socket class object(AF_INET=ipv4 use kortesti, sock_stream boltese tcp use kortesi, )
    #sock_dgram for udp 
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST}:{PORT}")
    except:
        print(f"Unable to bind to host  {HOST} and {PORT}")
        #bind korte parbe na jokhon host ar port bind korte parbe na

    #SET SERVER LIMIT
    server.listen(LISTENER_LIMIT)

    #this while will keep listening to client connections

    while True:
        client,address=server.accept()
        print(f"Successfully connected to client :{address[0]}:{address[1]}")


        #we want our function to run concurrently with the server side function

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__=='__main__':
    main()
#main function will be called if the server.py
#was called directly, else if called from a module
#it won't be called


