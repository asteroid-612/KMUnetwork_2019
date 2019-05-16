# -*- coding: utf-8 -*-
import socket
import os
import sys
import select

# 참고한 reference 주소============
# https://www.geeksforgeeks.org/simple-chat-room-using-python/
# https://medium.com/vaidikkapoor/understanding-non-blocking-i-o-with-python-part-1-ec31a2e2db9b
# https://itholic.github.io/python-select/
# https://scienceofdata.tistory.com/entry/Python-select-%ED%95%A8%EC%88%98%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EA%B0%84%EB%8B%A8%ED%95%9C-%EC%97%90%EC%BD%94-%EC%84%9C%EB%B2%84%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8-%EC%98%88%EC%A0%9C
#================================

print("Student ID: 20171666")
print("Name: Lee SuJeong")

# client에서는 telnet localhost $(portnum)으로 접속한다.
# ex) "Connection Closed $(socket descriptor)"
# 클라이언트가 접속 종료해도 나머지 사용자들 간에는 채팅이 가능하다.

SIZE = 1024
chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# input을 통해서 tcp port를 알아온다.
port = int(sys.argv[1])
chat_sock.bind(('localhost', port))
chat_sock.setblocking(0)
# 클라이언트 요청이 들어오면 그 socket descriptor를 배열에 저장.
chat_sock.listen()
client_list = []
read_socket_list = [chat_sock]

while True:
    conn_read_socket_list, conn_write_socket_list, conn_except_socket_list = select.select(read_socket_list, [], [])
    for conn_read_socket in conn_read_socket_list:
        ## 아,,, 16개 이상 되게 하라는 말이지 제한을 두라는 말은 아닌것으로 ^^
##        if len(client_list) == 16:
##            print("No more clients allowed, reset client list")
##            client_list = []
##            break
        if conn_read_socket == chat_sock:
            # 새로운 소켓이 요청했어요 
            client_socket, client_addr = chat_sock.accept()
            a = str(client_socket)
            location = a.find('fd=')
            socket_num = a[location+3]
            print("connection from host ", client_addr[0], ', port ', client_addr[1], ', socket ', socket_num)
            read_socket_list.append(client_socket)
            client_list.append(client_socket)
        else:
            data = conn_read_socket.recv(SIZE)
            if data:
                # 데이터를 보내긴 했는데요 받을 친구가 없어요
                if len(client_list) == 1:
                    break
                # 데이터를 보냈고 받을 친구도 있네요 
                else:
                    for i in client_list:
                        if i != conn_read_socket:
                            i.send(data)
            else:
                # 연결이 끊겼어요 
                b = str(conn_read_socket)
                location_b = b.find('fd=')
                socket_num_b = b[location+3]
                print("Connection Closed ", socket_num_b)
                read_socket_list.remove(conn_read_socket)
                client_list.remove(conn_read_socket)
                conn_read_socket.close()
                break

