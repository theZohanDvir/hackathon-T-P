########## imports ##########
from socket import *
from _thread import *
import threading
from struct import *
from time import *
import traceback
import random

########## variables ##########
IP = '192.168.1.104'
IP = '192.168.14.6'
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
debug = 0
lstTCPs = {}
group1 = {}
group2 = {}

####### GROUP METHODS ########
def pick_random_group():
    global group1,group2
    groups = [group1,group2]
    if(len(group1)==len(group2)):
        return random.choice(groups)
    elif(len(group1)>len(group2)):
        return group2
    else:
        return group1

def groupCount(group):
    sum = 0
    for item in group.values():
        sum+=item
    return sum

def updateScore(team_name,cnt):
    global group1,group2
    if team_name in group1.keys():
        group1[team_name] = cnt
    else:
        group2[team_name] = cnt

def countGroupsScore(i):
    global group1,group2
    if i == 1:
        return groupCount(group1)
    elif i == 2:
        return groupCount(group2)

def winningGroup():
    global group1,group2
    if(groupCount(1)>=groupCount(2)):
        return 1
    else:
        return 2
####### /GROUP METHODS ########

def createGameMessage():
    global group1,group2
    a = "Welcome to Keyboard Spamming Battle Royale.\n"
    a = a + "Group 1:\n"
    for item in group1.keys():
        a = a + str(item) + "\n"
    a = a + "Group 2:\n"
    for item in group2.keys():
        a = a + str(item) + "\n"
    a = a + "Start pressing keys on your keyboard as fast as you can!!"
    return a

def groupTeamNames(i):
    global group1,group2
    a = ""
    if(i == 1):
        for item in group1.keys():
            a = a + str(item) + "\n"
    elif(i==2):
        for item in group2.keys():
            a = a + str(item) + "\n"
    return a


def createEndMessage():
    global group1,group2
    winnernumber = winningGroup()
    a = "Game over!\n"
    a = a + "Group 1 typed in " + str(countGroupsScore(1)) + " characters. Group 2 typed in " + str(countGroupsScore(2)) + " characters.\n"
    a = a + "Group " + str(winnernumber) + " wins!\n\n"
    a = a + "Congragulations to the winners:\n"
    a = a + groupTeamNames(winnernumber)
    return a

    

def TCPgame(connectionSocket,addr):
    global debug,timesUP,connected,teamsDict
    print("d:TCPgame starts") if debug >=2 else None
    cnt = 0
    team_name = connectionSocket.recv(bufsize).decode("utf-8")
    print("Team name is : " + team_name)
    teamsDict[team_name] = connectionSocket                 # add teamname and socket to dict
    pick_random_group()[team_name] = 0
    connected +=1
    while not timesUP:
        sleep(0.1)
        pass
    # while ( connected != minPlayers ):
    #     sleep(0.01)
    #     pass
    start_new_thread(reminderStart,())
    message = createGameMessage()
    connectionSocket.sendall(message.encode("utf-8")) # start game message
    while not reminderStartGame:
        response = (connectionSocket.recv(bufsize)).decode("utf-8")
        if ( response == "done"):
            break
        if (len(response)>0 and response != "b''"):
            cnt+=1
        # if (cnt %10 ==0 ):
        #     print(str(team_name) + ":" +str(cnt))
    updateScore(team_name,cnt)
    sleep(0.1)
    print ("your personal score: " + str(cnt))
    endgameMessage = createEndMessage()
    connectionSocket.sendall(endgameMessage.encode('utf-8') )
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
    global debug,connected,timesUP,minPlayers
    print("d:pyTCPServer started" + IP) if debug >= 2 else None
    TCPserverSocket = socket(AF_INET, SOCK_STREAM)
    TCPserverSocket.bind((IP,portTCP))
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
    print("d:threaded_udp_message started") if debug >= 1 else None
    message = pack('IBH',4276993775,2,portTCP)
    for i in range(10):
        serverSocket.sendto(message, ('<broadcast>', portUDP))
        sleep(1)
        pass
    # connection closed 
    serverSocket.close() 

def main():
    global debug
    print("Server started, listening on IP address " + IP)
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    start_new_thread(threaded_udp_message,(serverSocket,))
    pyTCPServer()
    print("d:Server shutdown") if debug >= 1 else None

if __name__ == "__main__":
    main()