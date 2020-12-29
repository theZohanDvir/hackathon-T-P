from socket import *
from _thread import *
import threading
from struct import *

def pyUDPServer():
    print( "begin the server" )
    serverPort = 2010
    severSocket = socket(AF_INET,SOCK_DGRAM)
# Enable broadcasting mode
    severSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    severSocket.bind(('',serverPort))
    message = pack('IBH', 4276993775, 2, 2010)
    print(message)
    print(unpack('IBH',message))
    print ('Server started, listening on IP address 172.1.0.4')
    severSocket.sendto( message , ('255.255.255.255', 2010))
    print( "The server is ready to receive" )
    while 1:
        print( "wait for message" )
        messsage, clientAddress = severSocket.recvfrom(1024)
        timeout(1)
        print(unpack('IBH',message))
        # print ("message: " + str(messsage, 'utf-8') ) # need to be translated back to str from bytes
        # modifiedMessage = messsage.lower() # a func on the message
        # print (modifiedMessage)
        severSocket.sendto(b'good',clientAddress)
        pass

def pyThreadedTCPServer():
    print( "begin the server" )
    serverPort = 2010
    severSocket = socket(AF_INET,SOCK_DGRAM)
    severSocket.bind(('',serverPort))
    print( "The server is ready to receive" )
    while 1:
        print( "wait for message" )
        messsage, clientAddress = severSocket.recvfrom(2010)
        print ("message: " + str(messsage, 'utf-8') ) # need to be translated back to str from bytes
        modifiedMessage = messsage.lower() # a func on the message
        print (modifiedMessage)
        severSocket.sendto(modifiedMessage,clientAddress)
        pass

def main():
    print("Hello World! this is the server!!")
    pyUDPServer()

if __name__ == "__main__":
    main()
