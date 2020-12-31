########## imports ##########
from socket import *
from struct import unpack
from time import sleep
from pynput.keyboard import Listener
from threading import Timer


########## variables ##########
teamName = "KeybSpammers"
IP = '192.168.14.6'
IP = '192.168.1.104'
#IP = ''
host = gethostname()                           
portUDP = 13401
portTCP = 13601
bufsize = 2048
clientsocketTCPsend = None
localCNT = 0
debug = 0
##########

def on_press(key):
    global clientsocketTCPsend
    global localCNT
    print(str(key)) if debug >= 2 else None
    try:
        clientsocketTCPsend.sendall(str(key).encode('utf-8'))
        localCNT+=1
    except:
        print("e:not sent: " + str(key))
        pass
    

def TCPgame(clientsocket):
    global debug
    global clientsocketTCPsend
    print( "d:TCPgame start") if debug >= 1 else None
    clientsocketTCPsend = clientsocket
    print( "d:start game") if debug >= 1 else None
    groupName = input("Enter the group name: ")
    clientsocket.send(groupName.encode("utf-8")) # sends the name
    print(clientsocket.recv(bufsize).decode("utf-8")) # welcome and print start typeing
    with Listener(on_press=on_press) as listener:  # Create an instance of Listener
        Timer(10, listener.stop).start()
        print("test1") if debug >= 2 else None
        listener.join()  # Join the listener thread to the main thread to keep waiting for keys
    print("test2") if debug >= 2 else None
    try:
        print("d:start wait for server answer?") if debug >= 1 else None
        clientsocket.sendall(str("done").encode('utf-8'))
        print(clientsocket.recv(bufsize).decode("utf-8")) # waiting for score
    except:
        print("d:didn't get score from server.") if debug >= 1 else None
        pass
    print("d:localCNT: " + str(localCNT)) if debug >= 1 else None


def pyTCPClient(address, serverPort):
    print ("d: start TCP connection" )
    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect((address[0],serverPort))
    TCPgame(clientsocket)
    clientsocket.close()
    clientsocketTCPsend=0

def pyUDPClient():
    print("Client started, listening for offer requests...")
    clientSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    clientSocket.bind((IP, portUDP))
    data, addr = clientSocket.recvfrom(bufsize) # waiting for invaites
    print ("Received offer from " + addr[0] +", attempting to connect...")
    magicCookie, messageType, serverPort = unpack('IBH',data)
    if ( magicCookie != 4276993775 or messageType != 2):
        print( " magicCookie != 4276993775 and messageType != 2 ")
    clientSocket.close()
    pyTCPClient(addr, serverPort)
    

def main():
    global debug
    print("d: client begin") if debug >=1 else None
    address = pyUDPClient()
    print("d: client ends") if debug >=1 else None


if __name__ == "__main__":
    main()
