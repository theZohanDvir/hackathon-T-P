########## imports ##########
from socket import *
from _thread import *
import threading
from struct import *
from time import *
import traceback

########## variables ##########
IP = '192.168.1.104'
# IP = ''
host = gethostname()                           
portUDP = 13401
portTCP = 13601
bufsize = 1024

def TCPgame():
    print( "d:start game")
    print( "Welcome to Keyboard Spamming Battle Royale.")

def pyTCPServer():
    # todo: add tuple for difrent TCP , 2 groups
    TCPserverSocket = socket(AF_INET, SOCK_STREAM)
    TCPserverSocket.bind((IP,portTCP))
    # queue up to 5 requests
    TCPserverSocket.listen(3)
    while True:
        # establish a connection
        connectionSocket ,addr = TCPserverSocket.accept() #stops until
        response = connectionSocket.recv(bufsize)
        print("Got a connection from %s" % str(addr))
        connectionSocket.send(b'congragulations')

def threaded_udp_message(serverSocket): 
    message = pack('IBH',4276993775,2,portTCP)
    for i in range(11):
        serverSocket.sendto(message, ('<broadcast>', portUDP))
        print("d:message sent!")
        sleep(1)
        pass
    # connection closed 
    serverSocket.close() 

def main():
    print("d:Server started, listening on IP address" + IP)
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # serverSocket.bind((IP,portUDP))
    start_new_thread(threaded_udp_message,(serverSocket,))
    
    print ("d:The server is ready to receive")
        pyTCPServer()


if __name__ == "__main__":
    main()