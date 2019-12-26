# -*- coding: utf-8 -*-
import socket
import time
import cv2
import numpy
import json

import threading

class recFaceRlt(threading.Thread):
    def __init__(self, signal =None, decodeQueue = None):
        super(recFaceRlt, self).__init__()
        self.queue = decodeQueue
        self.signal = signal  #threading.Event()

    def recvall(self, sock, count):
        buf = b''  # buf是一个byte类型
        while count:
            # 接受TCP套接字的数据。数据以字符串形式返回，count指定要接收的最大数据量.
            newbuf = sock.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def recvalle(self, sock):
        buf = b''  # buf是一个byte类型
        while True:
            newbuf = sock.recv(3000)
            # print(newbuf[-3:])
            if newbuf[-3:] == b'END':
                print(newbuf[-3:])
                buf += newbuf[:-3]
                break
            # print(len(newbuf))
            buf += newbuf
        return buf

    # def ReceiveVideo():
    def run(self):
        # IP地址'0.0.0.0'为等待客户端连接
        address = ('0.0.0.0', 8002)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(address)
        s.listen(1)

        while True:  # 循环轮询socket状态，等待访问
            conn, addr = s.accept()
            try:
                # conn.settimeout(50)
                while True:
                    try:
                        info = self.recvalle(conn)
                        try:
                            info = str(info, encoding='utf-8')
                            recData = eval(info) #接收的info为字典格式时才需要用eval解析
                            print('rec')
                            for key, value in recData.items():
                                if key == 'ids':
                                    for item in value:
                                        print(item)
                            conn.sendall(bytes('succeed', encoding='utf-8'))
                            stringData = recData['data']  # 根据获得的文件长度，获取图片文件
                            data = numpy.frombuffer(stringData, numpy.uint8)  # 将获取到的字符流数据转换成1维数组
                            decimg = cv2.imdecode(data, cv2.IMREAD_COLOR)  # 将数组解码成图像
                            decinfo = {
                                'data': decimg,
                                'ids':  recData['ids'],
                                'names':recData['names'],
                                'boxes': recData['boxes'],
                            }
                            if self.queue is not None:
                                self.queue.add(decinfo)

                            if self.signal is not None:
                                self.signal.set()
                            # cv2.imwrite('messigray.png', decimg)
                            # cv2.imshow('SERVER', decimg)  # 显示图像
                            # k = cv2.waitKey(0)# & 0xff
                            # if k == 27:
                            #     break
                        except Exception as e:
                            print("except")
                            conn.sendall(bytes('except', encoding='utf-8'))
                    except Exception as e:
                        print("recerr")
                        break
            except socket.timeout:
                print('timeout')
            conn.close()
            print('close')

        s.close()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # ReceiveVideo()
    reth = recFaceRlt()
    reth.start()
