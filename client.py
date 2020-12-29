from server import openTCPConnection
from socket import *

def openTCPConnection(serverAddress):
    print("TCP client connection")
    serverPort=2010
    serverName= '192.168.14.6' #the IP you want to connect to
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(serverAddress)
    message = b"UDP 2"
    clientSocket.send(message)
    modifiedMessage = clientSocket.recv(2055)
    print(" from TCP: " + str(modifiedMessage, 'utf-8') )
    clientSocket.close()


def pyUDPClient():
    print("in client function")
    serverPort=2010
    serverName= '192.168.14.6' #the IP you want to connect to
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    message = b"UDP 1"
    clientSocket.sendto(message,(serverName,serverPort))
    modifiedMessage, serverAddress = clientSocket.recvfrom(2055)
    print(modifiedMessage)
    print (serverAddress)
    if ( str(modifiedMessage, 'utf-8') == "udp 1" ):
        print ( "start TCP" )
        openTCPConnection(serverAddress)
    clientSocket.close()


def main():
    print("client begin")
    pyUDPClient()

if __name__ == "__main__":
    main()
