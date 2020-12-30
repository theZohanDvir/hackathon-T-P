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
reminderStartGame = False

def TCPgame(connectionSocket,addr):
    global timesUP
    cnt = 0
    connectionSocket.sendall(b"Welcome to Keyboard Spamming Battle Royale.")
    team_name = connectionSocket.recv(bufsize)
    print("Team name is : " + str(team_name))
    # add teamname and socket to dict
    global teamsDict
    teamsDict[team_name] = connectionSocket
    print("Got a connection from %s" % str(addr))
    # print(timesUP)
    while not timesUP:
        sleep(0.1)
        pass
    print("game is live from port " + str(addr[1]))
    connectionSocket.send(b"Start pressing keys on your keyboard as fast as you can!!")
    while not reminderStartGame:
        response = str(connectionSocket.recv(bufsize))
        print("r:" + response)
        if ( response == "b''"):
            break
        if (len(response)>0 and response != "b''"):
            cnt+=1
        if (cnt %10 ==0 ):
            print(str(team_name) + ":" +str(cnt))
    print (("finel score: " + str(cnt)).encode('utf-8'))
    connectionSocket.send(("your score is: " + str(cnt)).encode('utf-8') )
    sleep(1)
    print("TCP is closing connection from port %s" % str(addr))
    connectionSocket.close()

def reminder():
    sleep(10)
    global timesUP
    timesUP = True

def reminderStart():
    sleep(10)
    global reminderStartGame
    reminderStartGame = True

def pyTCPServer():
    global timesUP
    # todo: add tuple for difrent TCP , 2 groups
    TCPserverSocket = socket(AF_INET, SOCK_STREAM)
    TCPserverSocket.bind((IP,portTCP))
    # queue up to 5 requests
    TCPserverSocket.listen(3)
    lstTCPs = {}
    start_new_thread(reminder,())
    while (not timesUP):
        # establish a connection
        connectionSocket ,addr = TCPserverSocket.accept() #stops until
        lstTCPs[connectionSocket] = addr
        if ( len(lstTCPs) > 0 ):
            for targCon in lstTCPs:
                try:
                    start_new_thread(TCPgame,(targCon,lstTCPs[targCon]))
                    pass
                except connectionSocket.timeout:
                    pass
                pass
            start_new_thread(reminderStart,())
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