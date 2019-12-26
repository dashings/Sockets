import socket
import cv2
import numpy
import time
import sys

def SendVideo():

    # file = os.listdir('./query')
    # dir =os.path.join('./query',file[0])
    address = ('127.0.0.1', 9998)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    capture = cv2.VideoCapture('d:/VID_20190404_101400.mp4') 
    ret, frame = capture.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]

    index =0
    num =0
    while ret:
        # time.sleep(5)
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        strlen  = struct.pack("i",len(stringData))
        sock.send(strlen)
        sock.send(stringData)
        
        ret, frame = capture.read()

    sock.close()


if __name__ == '__main__':
    SendVideo()
