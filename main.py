import socket

from mainWindowLogic import MainWindowLogic
from SocketCommunication.JavaConnect import SeverThreading

if __name__ == '__main__':
    main1 = MainWindowLogic()

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()

    port = 50001

    serversocket.bind((host, port))

    serversocket.listen(5)

    myaddr = serversocket.getsockname()

    print("服务器地址：%s" % str(myaddr))

    # startDevice = SeverThreading(serversocket,self)
    # startDevice.Aaa()
    # pass
    while True:
        clientsocket, addr = serversocket.accept()
        print("连接地址：%s" % str(addr))

        try:
            startDevice = SeverThreading(clientsocket, main1)
            startDevice.start()
            pass
        except Exception as identifier:
            print(identifier)
            pass
        pass

    serversocket.close()
    pass