from server import openTCPConnection
from socket import *

pavelIP = '192.168.1.104'

def openTCPConnection(serverAddress):
    print("TCP client connection")
    serverPort=2010
    serverName= pavelIP #the IP you want to connect to
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(serverAddress)
    message = b"UDP 2"
    clientSocket.send(message)
    modifiedMessage = clientSocket.recv(2055)
    print(" from TCP: " + str(modifiedMessage, 'utf-8') )
    clientSocket.close()


def pyUDPClient():
    print("in client function")


    # serverPort=2010
    # serverName = pavelIP #the IP you want to connect to
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    clientSocket.bind(('',2010))

    message, serverAddress = clientSocket.recvfrom(1024)
    print(message)

    # message = b"HEY Tomer its ron and we connect server to client"
    # clientSocket.sendto(message,(serverName,serverPort))
    
    clientSocket.close()


def main():
    print("client begin")
    pyUDPClient()
