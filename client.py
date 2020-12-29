
from socket import *


def pyUDPClient():
    print("in client function")
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

    s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    # get local machine name
    host = gethostname()                           

    port = 9999

    # connection to hostname on the port.        

    s.bind(('', port))
    
    data, addr = s.recvfrom(1024)
    print("received message: %s"%data)  
    
    s.close()                  

    clientsocket = socket(AF_INET, SOCK_STREAM)
    clientsocket.connect(addr)
    clientsocket.send('i need you i want you')

    response = clientSocket.recv(1024)

    print("The time got from the server is %s" % response.decode('ascii'))


def main():
    print("client begin")
    pyUDPClient()

if __name__ == "__main__":
    main()
