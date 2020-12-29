from socket import *
from _thread import *
import threading
from struct import *
from time import *

# def openTCPConnection( clientAddress ):
#     print( "begin TCP " )
#     serverPort = 2010
#     serverSocket = socket(AF_INET,SOCK_STREAM)
#     serverSocket.bind(('',serverPort))
#     serverSocket.listen(1)
#     print( "The server is ready to receive" )
#     while 1:
#         print( "wait for TCP message" )
#         connectionSocket, addr = serverSocket.accept()
#         print ( connectionSocket )
#         print ( addr )
#         sentence = connectionSocket.recv(2010)
#         connectionSocket.send(sentence.lower())
#         connectionSocket.close()

# def pyUDPServer():
#     print( "begin the server" )
#     serverPort = 2010
#     severSocket = socket(AF_INET,SOCK_DGRAM)
# # Enable broadcasting mode
#     severSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
#     # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     severSocket.bind(('',serverPort))
#     message = pack('IBH', 4276993775, 2, 2010)
#     print(message)
#     print(unpack('IBH',message))
#     print ('Server started, listening on IP address 172.1.0.4')
#     print( "The server is ready to receive" )
#     while 1:
#         severSocket.sendto( message , ('255.255.255.255', 2010))
#         sleep(1)
#         # print( "wait for message" )
#         # messsage, clientAddress = severSocket.recvfrom(1024)
#         # timeout(1)
#         # print(unpack('IBH',message))
#         # # print ("message: " + str(messsage, 'utf-8') ) # need to be translated back to str from bytes
#         # # modifiedMessage = messsage.lower() # a func on the message
#         # # print (modifiedMessage)
#         # severSocket.sendto(b'good',clientAddress)
#         # pass

# def pyThreadedTCPServer():
#     print( "begin the server" )
#     serverPort = 2010
#     severSocket = socket(AF_INET,SOCK_DGRAM)
#     severSocket.bind(('',serverPort))
#     print( "The server is ready to receive" )
#     while 1:
#         print( "wait for UDP message" )
#         messsage, clientAddress = severSocket.recvfrom(2010)
#         print ("message: " + str(messsage, 'utf-8') ) # need to be translated back to str from bytes
#         if ( str(messsage, 'utf-8') == "UDP 1" ):
#             severSocket.sendto(messsage.upper(),clientAddress)
#             openTCPConnection( clientAddress )
#         # modifiedMessage = messsage.upper() # a func on the message
#         #print (modifiedMessage)
#         #serverSocket.sendto(modifiedMessage,clientAddress)
#         pass

# server.py 



def pyUDPServer2():
    # create a socket object
    serversocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    # get local machine name
    host = gethostname()                           
    port = 9999                                           
    # # bind to the port
    # serversocket.bind(('', port))                                 
    # Enable broadcasting mode
    serversocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    serversocket.settimeout(0.2)
    message = b"your very important message"
    for i in range(11):
        serversocket.sendto(message, ('<broadcast>', 9999))
        print("message sent!")
        sleep(1)
    # queue up to 5 requests
    serversocket.listen(3)                                           
    while True:
        # establish a connection
        clientsocket,addr = serversocket.accept()      
        print("Got a connection from %s" % str(addr))
        currentTime = ctime(time()) + "\r\n"
        clientsocket.send(currentTime.encode('ascii'))
        sleep(2)

def main():
    print("Hello World! this is the server!!")
    pyUDPServer2()

if __name__ == "__main__":
    main()
