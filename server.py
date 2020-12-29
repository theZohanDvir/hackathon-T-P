########## imports ##########
from socket import *
from _thread import *
import threading
from struct import *
from time import *

########## variables ##########
#IP = '192.168.14.6'
IP = ''
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

def pyUDPServer():
    # create a socket object
    serverSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    #serverSocket.bind((IP,portUDP))
    print ("d:The server is ready to receive")
    message = pack('IBH',4276993775,2,portTCP)
    for i in range(11):
        serverSocket.sendto(message, ('<broadcast>', portUDP))
        print("d:message sent!")
        sleep(1)
        pass

def main():
    print("d:Server started, listening on IP address" + IP)
    # todo: need perallel
    while 1:
        pyUDPServer()
        pyTCPServer()

if __name__ == "__main__":
    main()
