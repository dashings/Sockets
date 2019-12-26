# -*- coding: utf-8 -*-
import socket
import cv2
import numpy
import time
import sys
import json
import os

def SendVideo():

    # file = os.listdir('./query')
    # dir =os.path.join('./query',file[0])
    # address = ('192.168.201.147', 8002)
    # address = ('127.0.0.1', 8002)
    address = ('192.168.201.26', 8002)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    # capture = cv2.VideoCapture('reid.mp4') #'reid.mp4'
    capture = cv2.VideoCapture(0) #'reid.mp4'
    ret, frame = capture.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]

    index =0
    num =0
    while ret:
        # time.sleep(5)
        if index >200:
            num +=1
            index = 0
            time.sleep(200)
        index +=1
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        # print(len(stringData))
        info = {
             'ids': [num],
             'data': stringData,
             'names':['test','test1'],
             # 'boxes':[u'标题1',u'标题2',u'标题3'],
             'boxes':[[1,2,3,4],[1,2,3,4]],
        }
        # print(info.__sizeof__())

        aa = str.encode(repr(info)) # 此处info为字典，才需要用repr序列化
        print(len(aa))
        # sock.sendall(aa.rjust(35000))
        sock.sendall(aa)
        sock.send(str.encode('END'))


        # answer = 'except'
        # while answer != 'succeed':
        #     time.sleep(1)
        #     aa= str.encode(repr(info))
        #     print(len(aa))
        #     # sock.sendall(aa.rjust(35000))
        #     sock.sendall(aa)
        #     sock.send(str.encode('END'))
        #     try:
        #         answer = sock.recv(100)
        #         answer = str(answer, encoding='utf-8')
        #         print('answer = %s' % answer)
        #     except Exception as e:
        #         answer = 'except'
        ret, frame = capture.read()

    sock.close()


if __name__ == '__main__':
    SendVideo()
