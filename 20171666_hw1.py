import socket
import os

# 작동해야하는 명령어 두개 
# wget netapp.cs.kookmin.ac.kr 80 /web/member/palladio.JPG
# wget s3.amazonaws.com 80 /american-rivers-website/wp-content/uploads/2015/09/22182724/NW-rivers-threatened-by-Red-Flat-Systems_KenMorrish-header-713x629.jpg

# 참고한 stack overflow 주소 
# https://stackoverflow.com/questions/47658584/implementing-http-client-with-sockets-without-http-libraries-with-python
# https://stackoverflow.com/questions/29110620/how-to-download-file-from-local-server-in-python

# 무조건 맨 위에 한번 프린트 해야하는 부분. 
print('Student ID : 20171666')
print('Name : Sujeong Lee')

# def PROMPT()를 만들어서 계속 input을 받는 애를 만든다. string으로 받으면 될 듯
def PROMPT():
    n = str(input("> "))
    return n

# main body=================================================================

# 예외처리 2가지 -----------------------------------------------------
# 서버에 연결이 안되면 서버에 연결이 안된다고 메세지를 출력
# cannot connect to server ""
# HTTP response status가 200이 아니면, 코드를 출력하고 프롬프트를 다시 출력 
# 404 Not Found
# -------------------------------------------------------------------

while True:
    str_in = PROMPT()
    str_in_list = str_in.split()
    if str_in == "":
        continue
    if str_in_list[0] == "quit":
        break
    if str_in_list[0] == "wget":
        download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (str_in_list[1], int(str_in_list[2]))
        # 서버에 연결할 수 없는 경우는 서버에 연결할 수 없다는 메세지를 프롬프트에 출력한다.
        try:
            download_socket.connect(server_address)
            message = "GET " + str_in_list[3] + " HTTP/1.0\r\n" 
            message += "Host: " + str_in_list[1] + "\r\n"
            message += "User-agent: HW1/1.0\r\n"
            message += "ID: 20171666\r\n"
            message += "Name: Sujeong Lee\r\n"
            message += "Connection: close\r\n\r\n"
            byte_message = message.encode()
            download_socket.sendall(byte_message)

            data = b''
            # \r\n\r\n이 나올때까지 계속 받는다. 
            while b'\r\n\r\n' not in data:
                data += download_socket.recv(1)

            # 받은 data를 \r\n\r\n빼고 decode한다. 그러면 header가 나옴.
            header = data[:-4].decode()
            # status code 가 200이 아니면 status를 print 하고 끝내도록 만든다. 
            header_list = header.split("\n")
            if header_list[0].find('2') == -1:
                print(header_list[0][9:])
            else:
                # headers를 dictionary로 만든다. ': '로 split해서 key로 만들면 된다.
                headers = dict([i.split(': ') for i in header.splitlines()[1:]])
                # 거기서 Content-Length를 찾아서 integer로 변환하면 길이가 나온다. 
                content_length = int(headers.get('Content-Length', 0))
                print("Total Size ",content_length," bytes")
                # 이제 다운로드
                filename = str_in_list[3].split("/")[-1]
                percentlist = [1,2,3,4,5,6,7,8,9]
                with open(os.path.join(os.getcwd(), filename), 'wb') as file_to_write:
                    file_data = download_socket.recv(content_length)
                    while len(file_data) != content_length:
                        percent = int(len(file_data)/content_length*100)
                        if percent//10 in percentlist:
                            percentlist.remove(percent//10)
                            print("Current Downloading ", len(file_data),"/", content_length, "(bytes) ",
                            percent, "%")
                        file_data += download_socket.recv(content_length)
                    print("Download Complete: ", filename, len(file_data), "/", content_length)
                    file_to_write.write(file_data)
                    file_to_write.close()
                download_socket.close()
        # 서버에 연결 안되면 처리하는 부분.
        except:
            print(str_in_list[1], " : unknown host")
            print("cannot connect to server ", str_in_list[1], " ", str_in_list[2])
        
        
