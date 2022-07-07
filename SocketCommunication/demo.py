import json
import socket
import sys
import threading


class SeverThreading(threading.Thread):
    def __init__(self, clientsocket, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding

    def receiveMsg(self):
        # 接受数据
        msg = ''
        # 从Java端读取recvsize个字节
        rec = self._socket.recv(self._recvsize)
        # 解码成字符串
        msg += rec.decode(self._encoding)
        print("解码后数据：")
        print(msg)

        # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕
        # 所以需要自定义协议标志数据接受完毕
        if msg.strip().endswith('over'):
            msg = msg[:-4]

        # 将字符串解析成JSON格式数据
        re = json.loads(msg)
        # re = {'type':'listenProductPosition'}
        print("解析成JSON数据：")
        print(re)
        return re

    def run(self):
        print("开启线程.....")

        try:
            # 接受数据
            msg = ''
            # 从Java端读取recvsize个字节
            rec = self._socket.recv(self._recvsize)
            # 解码成字符串
            msg += rec.decode(self._encoding)
            print("解码后数据：")
            print(msg)

            # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕
            # 所以需要自定义协议标志数据接受完毕
            if msg.strip().endswith('over'):
                msg = msg[:-4]

            # 将字符串解析成JSON格式数据
            re = json.loads(msg)
            # re = {'type':'listenProductPosition'}
            print("解析成JSON数据：")
            print(re)
            if re['type'] == 'startConveyor':
                re['type'] = 'startConveyorReply'
                re["content"] = "ok"
                re['statusCode'] = 200

            sendmsg = json.dumps(re)
            print("修改JSON数据并发送：")
            print(sendmsg)

            # 发送字符串数据给Java端
            self._socket.send(("%s" % sendmsg + "\r\n").encode(self._encoding))
            sys.stdout.flush()

            self._socket.close()
            print('----------')
            pass
        except Exception as identifier:
            re['statusCode'] = 500
            sendmsg = json.dumps(re)

            self._socket.send(("%s" % sendmsg + "\r\n").encode(self._encoding))
            # self._socket.send("500".encode(self._encoding))

            print(identifier)
            pass
        finally:
            self._socket.close()

if __name__ == '__main__':
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
    # while True:
    clientsocket, addr = serversocket.accept()
    print("连接地址：%s" % str(addr))

    try:
        startDevice = SeverThreading(clientsocket)
        startDevice.start()
        pass
    except Exception as identifier:
        print(identifier)
        pass
    pass

    serversocket.close()
    pass