import socket
import os
import threading


def deal_client_request(ip_port, service_client_socket):
    #  output after successful connection “ client connection successful ” and the client's ip and port
    print(" client connection successful ", ip_port)
    #  receive request information from the client
    file_name = service_client_socket.recv(1024)
    #  decoding
    file_name_data = file_name.decode("utf-8")
    #  determine if the file exists
    if os.path.exists(file_name_data):
        # output file bytes
        fsize = os.path.getsize(file_name_data)
        # convert to megabytes
        fmb = fsize / float(1024 * 1024)
        # file information to transfer
        senddata = " the file name ：%s   the file size ：%.2fMB" % (file_name_data, fmb)
        # send and print file information
        service_client_socket.send(senddata.encode("utf-8"))
        print(" request file name ：%s   the file size ：%.2f MB" % (file_name_data, fmb))
        # accept whether the customer needs to download
        options = service_client_socket.recv(1024)
        if options.decode("utf-8") == "y":
            #  open the file
            with open(file_name_data, "rb") as f:
                # 　 calculate the total number of packets
                nums = fsize / 1024
                # 　 the number of packets currently transmitted
                cnum = 0

                while True:
                    file_data = f.read(1024)
                    cnum = cnum + 1
                    jindu = cnum / nums * 100

                    print(" currently downloaded ：%.2f%%" % jindu, end="\r")
                    if file_data:
                        #  once the data is read, it is sent to the client
                        service_client_socket.send(file_data)
                    #  when the data is finished, exit the loop
                    else:
                        print(" the requested file data is sent ")
                        break
        else:
            print(" download the cancel ！")
    else:
        print(" the downloaded file does not exist ！")
    #  close the socket on the service's current client
    service_client_socket.close()


if __name__ == '__main__':
    #  change the working directory to the data directory
    os.chdir("./data")
    #  create a socket
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #  bind port number
    tcp_server_socket.bind(("", 3356))
    #  set listening to change an active socket to a passive socket
    tcp_server_socket.listen(128)

    #  a circular call to accept allows multiple clients to connect simultaneously ， download files simultaneously with multiple clients
    while True:
        service_client_socket, ip_port = tcp_server_socket.accept()
        #  print socket size after successful connection
        # print(id(service_client_socket))

        #  create child thread
        sub_thread = threading.Thread(target=deal_client_request, args=(ip_port, service_client_socket))
        #  start child thread
        sub_thread.start()
