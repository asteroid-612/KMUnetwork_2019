# -*- coding: utf-8 -*-
import socket
import os
import sys
from pathlib import Path

# 참고한 references 주소==========================================================
# https://stackoverflow.com/questions/3112980/making-python-sockets-visible-for-outside-world
# https://stackoverflow.com/questions/28521261/python-socket-programming-simple-web-server
# https://medium.com/python-pandemonium/python-socket-communication-e10b39225a4c
# https://stackoverflow.com/questions/40144535/send-file-to-a-browser-using-python-socket-programming
# https://stackoverflow.com/questions/27594464/socket-sendall-not-sending-to-all-connected-clients
#

# 무조건 맨 위에 한번 프린트 해야하는 부분.=======================================
print('Student ID : 20171666')
print('Name : Sujeong Lee')

# input 으로 포트 번호를 받아와야한다. 
# 이 포트넘버를 넣어서 http://localhost:<포트넘버> 에 웹서버(소켓)를 만들어줘야한다.
# 포트를 통해서 브라우저에서 요청한 파일을 소켓을 통해서 보내주는 형식

host = 'localhost'
port = int(sys.argv[1])

web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web_socket.bind((host, port))
web_socket.listen(1)

while True:
    # print("waiting for a connection")
    # establish connection 
    connection, conn_addr = web_socket.accept()
    a = str(connection)
    location = a.find('fd=')
    socket_num = a[location+3]
    
    print('Connection : Host IP ', conn_addr[0], ', Port', conn_addr[1], ', socket', socket_num)
    try:    
        # 데이터를 받아와서 decode한 다음에 프린트하는 부분.======================
        while True:
            data = connection.recv(1024)
            # print(data)
            decoded_data = data.decode('utf8')
            print(decoded_data)
            break
        
        # 파일의 이름을 잘라오는 부분.============================================
        file_name_end = decoded_data.find('l') + 1
        file_name = decoded_data[5:file_name_end]
        # 파일의 위치를 만들고, 실제로 존재하는 파일인지를 확인하는 부분 =========
        file_location = Path(os.getcwd() + decoded_data[4:file_name_end])
        # print(file_location)
        # 실제로 존재하는 파일일때, response 200 이고 file을 보내줘야한다.========
        if file_location.is_file():
            file = open(file_name, 'rb')
            read_f = file.read()
            length = len(read_f)
            # print(length)
            suc_mesg = "HTTP/1.0 200 OK\r\n"
            suc_mesg += "Connection: close\r\n"
            suc_mesg += "ID: 20171666\r\n"
            suc_mesg += "Name: Sujeong Lee\r\n"
            suc_mesg += "Content-Length: " + str(length) + "\r\n"
            suc_mesg += "Content-Type: text/html\r\n\r\n"
            suc_mesg = suc_mesg.encode()
            header_len = len(suc_mesg)
            suc_mesg += read_f
            # print(suc_mesg.encode())
            try:
                connection.sendall(suc_mesg)
                whole_len = len(suc_mesg)
                print("finish ", length," ", whole_len-header_len)
                # connection.close()
            except:
                print("something happened")
        else: # 폴더안에 그런 파일이 없을때. 
            fail_mesg = "HTTP/1.0 404 NOT FOUND\r\n"
            fail_mesg += "Connection: close\r\n"
            fail_mesg += "ID: 20171666\r\n"
            fail_mesg += "Name: Sujeong Lee\r\n"
            fail_mesg += "Content-Length: 0\r\n"
            fail_mesg += "Content-Type: text/html\r\n\r\n"
            b_fail_mesg = fail_mesg.encode()
            connection.sendall(b_fail_mesg)
            # connection.close()
            print("Server Error : No such file ./",file_name, " !")
        
    except:
        # print("hey ,,, what happened")
        # connection.send(b'404 Not Found')
        # connection.close()
        break
web_socket.close()
