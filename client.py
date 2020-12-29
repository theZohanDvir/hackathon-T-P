########## imports ##########
from socket import *
from struct import unpack
from time import sleep

########## variables ##########
teamName = "KeybSpammers"
IP = '192.168.1.104'
IP = '192.168.14.6'
#IP = ''
host = gethostname()                           
portUDP = 13401
portTCP = 13601
bufsize = 2048
##########

def TCPgame(clientsocket):
    print( "d:start game")
    response = clientsocket.recv(bufsize) # waiting for the game start message
    print (response.decode("utf-8"))
    while 1:
        response = clientsocket.recv(bufsize) # waiting for the game start message
        print ("response from TCP: " + response.decode("utf-8"))


def pyTCPClient(address, serverPort):
    print ("d: start TCP connection" )
    # TCP connection   
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((address[0],serverPort))
    clientsocket.send(b'i need you i want you')
    TCPgame(clientsocket)
    clientsocket.close()

def pyUDPClient():
    print("Client started, listening for offer requests...")
    clientSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # message = "d: i want to connect"
    # clientSocket.sendto(message,(IP,portUDP))
    # print ("d: waiting for message" )
    clientSocket.bind(("", portUDP))
    data, addr = clientSocket.recvfrom(bufsize) # waiting for invaites
    print ( "addr:" + str(addr))
    print ("Received offer from " + addr[0] +", attempting to connect...")
    magicCookie, messageType, serverPort = unpack('IBH',data)
    print ("magicCookie: " + str(magicCookie))
    print ("messageType: " + str(messageType))
    print ("server port: " + str(serverPort))
    if ( magicCookie != 4276993775 or messageType != 2):
        print( " magicCookie != 4276993775 and messageType != 2 ")
    clientSocket.close()
    pyTCPClient(addr, serverPort)
    # message = "i want to connect"
    # clientSocket.sendto(message,(IP,portUDP))
    # print ("d:" + addr )
    # print ("d:received message: %s"%data)
    

def main():
    print("d: client begin")
    address = pyUDPClient()
        


if __name__ == "__main__":
    main()
