########## imports ##########
from socket import *
from _thread import *
import threading
from struct import *
from time import *
import traceback

########## variables ##########
IP = '192.168.1.104'
IP = '192.168.14.6'
# IP = ''
host = gethostname()                           
portUDP = 13401
portTCP = 13601
bufsize = 1024

def TCPgame(connectionSocket,addr):
    cnt = 0
    print( "d:start game")
    print( "Welcome to Keyboard Spamming Battle Royale.")
    print("Got a connection from %s" % str(addr))
    connectionSocket.send(b'congragulations')
    groupNamge = connectionSocket.recv(bufsize)
    print(str(groupNamge))
    print("game is live from port " + str(addr[1]))
    while 1:
        response = str(connectionSocket.recv(bufsize))
        print("r:" + response)
        if ( response == "b''"):
            break
        if (len(response)>0 and response != "b''"):
            cnt+=1
        if (cnt %10 ==0 ):
            print(str(groupNamge) + ":" +str(cnt))
    print ("finel score: " + str(cnt))
    connectionSocket.send(("your score is: " + str(cnt)).encode('utf-8') )

def pyTCPServer():
    # todo: add tuple for difrent TCP , 2 groups
    TCPserverSocket = socket(AF_INET, SOCK_STREAM)
    TCPserverSocket.bind((IP,portTCP))
    # queue up to 5 requests
    TCPserverSocket.listen(3)
    lstTCPs = []
    while (len(lstTCPs) <= 2):
        # establish a connection
        connectionSocket ,addr = TCPserverSocket.accept() #stops until
        lstTCPs.append(connectionSocket)
        try:
            TCPgameThread = start_new_thread(TCPgame,(connectionSocket,addr))
            pass
        except connectionSocket.timeout:
            pass
    for con in lstTCPs:
        con.send(b"Start pressing keys on your keyboard as fast as you can!!")
        pass
        
        

def threaded_udp_message(serverSocket): 
    print("d:threaded_udp_message started")
    message = pack('IBH',4276993775,2,portTCP)
    for i in range(11):
        serverSocket.sendto(message, ('<broadcast>', portUDP))
        print("d:message sent!")
        sleep(1)
        pass
    # connection closed 
    serverSocket.close() 

def main():
    print("d:Server started, listening on IP address" + IP)
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # serverSocket.bind((IP,portUDP))
    udpTread = start_new_thread(threaded_udp_message,(serverSocket,))
    print ("udpTread: "+ str(udpTread))
    #tcpTread = start_new_thread(pyTCPServer,())
    pyTCPServer()
    # while 1:
    #     for i in threading.enumerate():
    #         if i.name == "MainThread":
    #             print ( i )

        

if __name__ == "__main__":
    main()