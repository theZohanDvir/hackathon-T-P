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
clientsocketTCPsend = 0
##########


def on_press(key):
    print("Key pressed: {0}".format(key))

def on_release(key):
    print("Key released: {0}".format(key))

def TCPgame(clientsocket):
    clientsocketTCPsend = clientsocket
    print( "d:start game")
    # groupName = input("Enter the group name: ")
    # clientsocket.send(bytes(groupName, 'utf-8'))
    response = clientsocket.recv(bufsize) # waiting for the game start message
    print (response.decode("utf-8"))
    with Listener(on_press=on_press, on_release=on_release) as listener:  # Create an instance of Listener
        Timer(10, listener.stop).start()
        listener.join()  # Join the listener thread to the main thread to keep waiting for keys
    # while 1:
    #     response = clientsocket.recv(bufsize) # waiting for the game start message
    #     print ("response from TCP: " + response.decode("utf-8"))


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
    while 1:
        address = pyUDPClient()
        


if __name__ == "__main__":
    main()
