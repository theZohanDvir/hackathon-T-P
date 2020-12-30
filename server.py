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
minPlayers = 2
connected = 0

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
    global connected
    connected +=1
    # print(timesUP)
    while not timesUP:
        sleep(0.1)
        pass
    while ( connected != minPlayers ):
        sleep(0.01)
        pass
    start_new_thread(reminderStart,())
    print("game is live from port " + str(addr[1]))
    connectionSocket.send(b"Start pressing keys on your keyboard as fast as you can!!")
    while not reminderStartGame:
        response = (connectionSocket.recv(bufsize)).decode("utf-8")
        # print("r:" + response)
        if ( response == "done"):
            print("d: break, send score")
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
    print("t-10")
    sleep(1)
    print("t-9")
    sleep(1)
    print("t-8")
    sleep(1)
    print("t-7")
    sleep(1)
    print("t-6")
    sleep(1)
    print("t-5")
    sleep(1)
    print("t-4")
    sleep(1)
    print("t-3")
    sleep(1)
    print("t-2")
    sleep(1)
    print("t-1")
    sleep(1)
    print("t")
    global reminderStartGame
    reminderStartGame = True

def pyTCPServer():
    global timesUP
    global minPlayers
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
        if ( len(lstTCPs) >= minPlayers ):
            for targCon in lstTCPs:
                try:
                    start_new_thread(TCPgame,(targCon,lstTCPs[targCon]))
                    pass
                except connectionSocket.timeout:
                    pass
                pass
        
        

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
        start_new_thread(threaded_udp_message,(serverSocket,))
        pyTCPServer()
        break
    print("d:Server shutdown")

        

if __name__ == "__main__":
    main()