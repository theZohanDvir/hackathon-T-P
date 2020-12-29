from socket import *
from time import *

def openTCPConnection( clientAddress ):
    print( "begin TCP " )
    serverPort = 2010
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print( "The server is ready to receive" )
    while 1:
        print( "wait for TCP message" )
        connectionSocket, addr = serverSocket.accept()
        print ( connectionSocket )
        print ( addr )
        sentence = connectionSocket.recv(2010)
        connectionSocket.send(sentence.lower())
        connectionSocket.close()

def pyUDPServer():
    print( "begin the server" )
    serverPort = 2010
    serverSocket = socket(AF_INET,SOCK_DGRAM)
    serverSocket.bind(('',serverPort))
    print( "The server is ready to receive" )
    while 1:
        print( "wait for UDP message" )
        serverSocket.sendto(b"test 1",('255.255.255.255',2010=> ))
        sleep(1)
        # messsage, clientAddress = serverSocket.recvfrom(2010)
        # print ("message: " + str(messsage, 'utf-8') ) # need to be translated back to str from bytes
        # if ( str(messsage, 'utf-8') == "UDP 1" ):
        #     serverSocket.sendto(messsage.lower(),clientAddress)
        #     openTCPConnection( clientAddress )
        # modifiedMessage = messsage.upper() # a func on the message
        #print (modifiedMessage)
        #serverSocket.sendto(modifiedMessage,clientAddress)
        pass


def main():
    print("Hello World! this is the server!!")
    pyUDPServer()

if __name__ == "__main__":
    main()
