########## imports ##########
from socket import *
from struct import unpack
from time import sleep
from pynput.keyboard import Listener
from threading import Timer


########## variables ##########
teamName = "KeybSpammers"
IP = '192.168.1.104'
IP = '192.168.14.6'
#IP = ''
host = gethostname()                           
portUDP = 13401
portTCP = 13601
bufsize = 2048
clientsocketTCPsend = None
##########


def on_press(key):
    print(str(key))
    global clientsocketTCPsend
    clientsocketTCPsend.sendall(str(key).encode('utf-8'))

def TCPgame(clientsocket):
    global clientsocketTCPsend
    clientsocketTCPsend = clientsocket
    print( "d:start game")
    response = clientsocket.recv(bufsize) # waiting for the game start message
    print (response.decode("utf-8"))
    groupName = input("Enter the group name: ")
    clientsocket.send(bytes(groupName, 'utf-8')) # sends the name
    with Listener(on_press=on_press) as listener:  # Create an instance of Listener
        Timer(10, listener.stop).start()
        listener.join()  # Join the listener thread to the main thread to keep waiting for keys
    gameScoreMessage = clientsocket.recv(bufsize)
    print(str(gameScoreMessage))


def pyTCPClient(address, serverPort):
    print ("d: start TCP connection" )
    # TCP connection   
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((address[0],serverPort))
    TCPgame(clientsocket)
    clientsocket.close()
    clientsocketTCPsend=0

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
    #while 1:
    address = pyUDPClient()
        


if __name__ == "__main__":
    main()
