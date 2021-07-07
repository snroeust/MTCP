#  multi-task file downloader client
import socket

if __name__ == '__main__':
    #  create a socket
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #  connect to the server
    server_ip = input(" input server ip ：")
    tcp_client_socket.connect((server_ip, 3356))
    #  send a request to download the file
    file_name = input(" please enter the file name to download ：")
    #  coding
    file_name_data = file_name.encode("utf-8")
    #  send file download request data
    tcp_client_socket.send(file_name_data)
    # 　 receive file information to download
    file_info = tcp_client_socket.recv(1024)
    #  file information decoding
    info_decode = file_info.decode("utf-8")
    print(info_decode)
    # get file size
    fileszie = float(info_decode.split('：')[2].split('MB')[0])
    fileszie2 = fileszie * 1024
    #  whether to download ？ the input ｙ　 confirm 　 the input ｑ  cancel
    opts = input(" whether to download ？(y  confirm 　q  cancel )")
    if opts == 'q':
        print(" download the cancel ！ program exits ")
    else:
        print(" is downloading 　》》》")
        # confirm to the server that it is downloading
        tcp_client_socket.send(b'y')

        #  write data to a file
        with open("./" + file_name, "wb") as file:
            # number of packets received so far
            cnum = 0

            while True:
                #  loop to receive file data
                file_data = tcp_client_socket.recv(1024)
                #  received data
                if file_data:
                    #  write data
                    file.write(file_data)
                    cnum = cnum + 1
                    jindu = cnum / fileszie2 * 100
                    print(" currently downloaded ：%.2f%%" % jindu, end="\r")
                #  receive complete
                else:
                    print(" download the end ！")
                    break
    #  close the socket
    tcp_client_socket.close()
