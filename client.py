from socket import *

pavelIP = '192.168.1.104'

def connect_to_server():
    print("in client function")


    # serverPort=2010
    # serverName = pavelIP #the IP you want to connect to
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    clientSocket.bind(('',2010))

    message, serverAddress = clientSocket.recvfrom(1024)
    print(message)

    # message = b"HEY Tomer its ron and we connect server to client"
    # clientSocket.sendto(message,(serverName,serverPort))
    
    clientSocket.close()


def main():
    print("client begin")
    connect_to_server()

if __name__ == "__main__":
    main()
