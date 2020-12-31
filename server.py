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
lstTCPs = {}

def TCPgame(connectionSocket,addr):
    global debug
    print("d:TCPgame starts") if debug >=2 else None
    global timesUP
    cnt = 0
    connectionSocket.sendall("Welcome to Keyboard Spamming Battle Royale.".encode())
    team_name = connectionSocket.recv(bufsize)
    print("Team name is : " + team_name.decode())
    # add teamname and socket to dict
    global teamsDict
    teamsDict[team_name] = connectionSocket
    print("Got a connection from %s" % str(addr))
    global connected
    connected +=1
    while not timesUP:
        sleep(0.1)
        pass
    while ( connected != minPlayers ):
        sleep(0.01)
        pass
    start_new_thread(reminderStart,())
    print("game is live from port " + str(addr[1]))
    connectionSocket.send("Start pressing keys on your keyboard as fast as you can!!".encode('utf-8'))
    while not reminderStartGame:
        response = (connectionSocket.recv(bufsize)).decode("utf-8")
        if ( response == "done"):
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
    print("d:TCPgame game end") if debug >=2 else None
    connected -=1

def reminder():
    sleep(10)
    global timesUP
    timesUP = True

def reminderStart():
    global debug
    print("d:t-10") if debug >= 1 else None
    sleep(1)
    print("d:t-9") if debug >= 1 else None
    sleep(1)
    print("d:t-8") if debug >= 1 else None
    sleep(1)
    print("d:t-7") if debug >= 1 else None
    sleep(1)
    print("d:t-6") if debug >= 1 else None
    sleep(1)
    print("d:t-5") if debug >= 1 else None
    sleep(1)
    print("d:t-4") if debug >= 1 else None
    sleep(1)
    print("d:t-3") if debug >= 1 else None
    sleep(1)
    print("d:t-2") if debug >= 1 else None
    sleep(1)
    print("d:t-1") if debug >= 1 else None
    sleep(1)
    print("d:t") if debug >= 1 else None
    global reminderStartGame
    reminderStartGame = True

lstTCPs={}
def acceptor(TCPserverSocket):
    global lstTCPs
    global minPlayers
    global timesUP
    # establish a connection
    while (not timesUP):
        print("d: Socket.accept()" + IP) if debug >= 2 else None
        connectionSocket ,addr = TCPserverSocket.accept() #stops until
        lstTCPs[connectionSocket] = addr

def pyTCPServer():
    global debug
    global connected
    print("d:pyTCPServer started" + IP) if debug >= 2 else None
    global timesUP
    global minPlayers
    # todo: add tuple for difrent TCP , 2 groups
    TCPserverSocket = socket(AF_INET, SOCK_STREAM)
    TCPserverSocket.bind((IP,portTCP))
    # queue up to 5 requests
    TCPserverSocket.listen(3)
    global lstTCPs
    start_new_thread(reminder,())
    start_new_thread(acceptor,(TCPserverSocket,))
    while (not timesUP):
        # note: minPlayers!!
        if ( len(lstTCPs) >= minPlayers ):
            print("d:if ( len(lstTCPs)") if debug >= 2 else None
            for targCon in lstTCPs:
                try:
                    start_new_thread(TCPgame,(targCon,lstTCPs[targCon]))
                    print("d:start_new_thread(TCPgame") if debug >= 2 else None
                    pass
                except errorExcept: # !!!!!!!!!!!!!!!!!
                    print("d:connectionSocket.timeout") if debug >= 2 else None
                    pass
                print("d:pass - pyTCPServer") if debug >= 2 else None
                pass
            break
    sleep(5)
    while True:
        sleep(1)
        if connected == 0:
            break
    print("d:pyTCPServer end" + IP) if debug >= 2 else None
        
        

def threaded_udp_message(serverSocket): 
    print("d:threaded_udp_message started")
    message = pack('IBH',4276993775,2,portTCP)
    for i in range(10):
        serverSocket.sendto(message, ('<broadcast>', portUDP))
        sleep(1)
        pass
    # connection closed 
    serverSocket.close() 

def main():
    global debug
    print("d:Server started, listening on IP address" + IP)
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    start_new_thread(threaded_udp_message,(serverSocket,))
    pyTCPServer()
    print("d:Server shutdown") if debug >= 1 else None

if __name__ == "__main__":
    main()