########## imports ##########
from socket import *
from _thread import *
import threading
from struct import *
from time import *
import traceback

########## variables ##########
IP = '192.168.14.6'
IP = '192.168.1.104'
# IP = ''
host = gethostname()                           
portUDP = 13401
portTCP = 13601
bufsize = 1024

teamsDict = {}

timesUP = False

def TCPgame(connectionSocket,addr):
    global timesUP
    cnt = 0
    connectionSocket.send(b"Welcome to Keyboard Spamming Battle Royale.")
    team_name = connectionSocket.recv(bufsize)
    print("Team name is : " + str(team_name))
    # add teamname and socket to dict
    teamsDict[team_name] = connectionSocket
    print("Got a connection from %s" % str(addr))
    # print(timesUP)
    while not timesUP:
        # print(timesUP)
        # sleep(1)
        pass
    print("game is live from port " + str(addr[1]))
    timesUP = False
    start_new_thread(reminder,())
    connectionSocket.send(b"Start pressing keys on your keyboard as fast as you can!!")
    while timesUP:
        response = connectionSocket.recv(bufsize)
        print(str(response))
        # if ( 'a' >= response and 'z' <=response):
        #     cnt+=1
        # if (cnt %10 ==0 ):
        #     print(str(groupNamge) + ":" +str(cnt))
    connectionSocket.close()

def reminder():
    sleep(10)
    global timesUP
    timesUP = True

def pyTCPServer():
    global timesUP
    # todo: add tuple for difrent TCP , 2 groups
    TCPserverSocket = socket(AF_INET, SOCK_STREAM)
    TCPserverSocket.bind((IP,portTCP))
    # queue up to 5 requests
    TCPserverSocket.listen(3)
    lstTCPs = []
    start_new_thread(reminder,())
    while (not timesUP):
        # establish a connection
        connectionSocket ,addr = TCPserverSocket.accept() #stops until
        lstTCPs.append(connectionSocket)
        try:
            TCPgameThread = start_new_thread(TCPgame,(connectionSocket,addr))
            pass
        except connectionSocket.timeout:
            pass
    # for con in lstTCPs:
    #     con.send(b"Start pressing keys on your keyboard as fast as you can!!")
    #     pass
        
        

def threaded_udp_message(serverSocket): 
    print("d:threaded_udp_message started")
    message = pack('IBH',4276993775,2,portTCP)
    for i in range(10):
        serverSocket.sendto(message, ('<broadcast>', portUDP))
        print("d:message sent!")
        sleep(1)
        pass
    # connection closed 
    serverSocket.close() 

def main():
    while True:
        print("d:Server started, listening on IP address" + IP)
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        # serverSocket.bind((IP,portUDP))
        start_new_thread(threaded_udp_message,(serverSocket,))
        #tcpTread = start_new_thread(pyTCPServer,())
        pyTCPServer()
        # while 1:
        #     for i in threading.enumerate():
        #         if i.name == "MainThread":
        #             print ( i )

        

if __name__ == "__main__":
    main()