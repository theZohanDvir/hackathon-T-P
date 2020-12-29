from socket import *
from _thread import *
import threading
from struct import *
from time import *


def pyUDPServer():

    # create a socket object
    serversocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    # get local machine name
    host = gethostname()                           
    port = 9999                                           
    # Enable broadcasting mode
    serversocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    serversocket.settimeout(0.2)
    message = b"your very important message"
    # for i in range(11):
        serversocket.sendto(message, ('<broadcast>', 9999))
        print("message sent!")
        sleep(1)
    serversocket.close()
    TCPserverSocket = socket(AF_INET, SOCK_STREAM)
    TCPserverSocket.bind(('',port))
    # queue up to 5 requests
    TCPserverSocket.listen(3)                                           

    while True:
        # establish a connection
        clientsocket,addr = TCPserverSocket.accept()      
        print("Got a connection from %s" % str(addr))
        clientsocket.send(b'congragulations')

    clientsocket.close()

def main():
    print("Hello World! this is the server!!")
    pyUDPServer()

if __name__ == "__main__":
    main()
