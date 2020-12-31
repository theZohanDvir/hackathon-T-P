########## imports ##########
from socket import *
from struct import unpack
from time import sleep
from pynput.keyboard import Listener
from threading import Timer


########## variables ##########
debug = 0
IP = '192.168.1.104'
IP = '192.168.14.6'
#IP = ''
host = gethostname()                           
portUDP = 13401
portTCP = 13601
bufsize = 2048
clientsocketTCPsend = None
localCNT = 0
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
    print( "d:TCPgame start") if debug >= 1 else None
    global clientsocketTCPsend
    clientsocketTCPsend = clientsocket
    print("d:"+ str(clientsocketTCPsend)) if debug >=1 else None
    print( "d:start game") if debug >= 1 else None
    groupName = input("Enter the group name: ")
    clientsocket.send(groupName.encode("utf-8")) # send the name
    response = clientsocket.recv(bufsize) # get ready messgae
    print (response.decode("utf-8"))
    print(str(clientsocket.recv(bufsize))) # print start typeing
    with Listener(on_press=on_press) as listener:  # Create an instance of Listener
        Timer(10, listener.stop).start()
        print("test1") if debug >= 2 else None
        listener.join()  # Join the listener thread to the main thread to keep waiting for keys
    print("test2") if debug >= 2 else None
    try:
        print("d:start wait for server answer?") if debug >= 1 else None
        clientsocket.sendall(str("done").encode('utf-8'))
        print(str(clientsocket.recv(bufsize))) # waiting for game over
        print(str(clientsocket.recv(bufsize))) # waiting for groups scores
        print(str(clientsocket.recv(bufsize))) # waiting for the winner group
        print(str(clientsocket.recv(bufsize))) # waiting for Congratulations
    except:
        print("d:didn't get score from server.") if debug >= 1 else None
        pass
    print("d:localCNT: " + str(localCNT)) if debug >= 1 else None


    # TCP connection
def pyTCPClient(address, serverPort):
    print ("d: start TCP connection" ) if debug >=1 else None
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
    print ( "d: addr:" + str(addr)) if debug >=1 else None
    print ("Received offer from " + addr[0] +", attempting to connect...")
    magicCookie, messageType, serverPort = unpack('IBH',data)
    print ("d:magicCookie: " + str(magicCookie)) if debug >=1 else None
    print ("d:messageType: " + str(messageType)) if debug >=1 else None
    print ("d:server port: " + str(serverPort)) if debug >=1 else None
    if ( magicCookie != 4276993775 or messageType != 2):
        print( " magicCookie != 4276993775 and messageType != 2 ") if debug >=1 else None
    clientSocket.close()
    pyTCPClient(addr, serverPort)
    # message = "i want to connect"
    # clientSocket.sendto(message,(IP,portUDP))
    # print ("d:" + addr )
    # print ("d:received message: %s"%data)
    

def main():
    global debug
    print("d: client begin") if debug >=1 else None
    address = pyUDPClient()
    print("d: client ends") if debug >=1 else None


if __name__ == "__main__":
    main()
