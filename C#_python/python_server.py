# -*- coding: utf-8 -*-
import socket

#创建一个socket对象
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
#sock.setblocking(1)
ip_port = ('127.0.0.1',9998)
#绑定ip和端口号
sock.bind(ip_port)
#sock.setblocking(1)
#设置最大连接数
sock.listen(5)


while True:
	#使用accept方法获取一个客户端连接
	#获取客户端的scoket对象conn和客户端的地址(ip、端口号)address
	conn,address = sock.accept()
	# 给客户端发信息
	send_data = 'Hello.'
	conn.sendall(str.encode(send_data))
	while True:
		try:
			# 接收客户端消息
			recv_data = conn.recv(1024)
      info = str(recv_data, encoding='utf-8')
			print(info)
			#print 'Client:', recv_data, ", Type:", type(recv_data), ", Equal:", (recv_data.replace("0x00", "") == 'start')
			#print 'Client:', recv_data[0:5], ", Type:", type(recv_data[0:5])
			# 如果收到start就开始调用统计代码
			if recv_data[0:5] == 'start':
				print( 'Ok, Starting...')
				# 开始调用统计代码输出结果到变量 result
				pass	
			#检测客户端发出退出指令，关闭连接
			if recv_data[0:4] == 'exit':
				break
			#s = input('Server:').strip()
			#if len(s) == 0:
			#	break
			#conn.send(bytes(s,encoding='utf-8'))
		except Exception as e:
			break

	# 关闭客户端的socket连接
	conn.close()
