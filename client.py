from sys import *
#from server import openTCPConnection
from socket import *


pavelIP = '192.168.1.104'
tomerIP = '192.168.14.6'

# def openTCPConnection(serverAddress):
#     print("TCP client connection")
#     serverPort=2010
#     serverName= pavelIP #the IP you want to connect to
#     clientSocket = socket(AF_INET,SOCK_STREAM)
#     clientSocket.connect(serverAddress)
#     message = b"UDP 2"
#     clientSocket.send(message)
#     modifiedMessage = clientSocket.recv(2055)
#     print(" from TCP: " + str(modifiedMessage, 'utf-8') )
#     clientSocket.close()


def pyUDPClient():
    print("in client function")
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # get local machine name
    host = gethostname()                           
    port = 9999
    # connection to hostname on the port.        
    s.bind(('', port))
    data, addr = s.recvfrom(1024)
    print("received message: %s"%data)  
    s.close()                  
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect(addr)
    clientsocket.send('i need you i want you')
    response = clientSocket.recv(1024)
    print (response)
    # serverPort=2010
    # serverName = pavelIP #the IP you want to connect to
    # clientSocket = socket(AF_INET,SOCK_DGRAM)
    # while 1:
    #     message, serverAddress = clientSocket.recvfrom(1024)
        # print(message)

    # message = b"HEY Tomer its ron and we connect server to client"
    # clientSocket.sendto(message,(serverName,serverPort))


def main():
    print("client begin")
    pyUDPClient()

if __name__ == "__main__":
    main()
