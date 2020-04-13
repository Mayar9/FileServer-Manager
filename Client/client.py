import socket
import os


def main():
    host = '127.0.0.1'
    port = 5000
    flag = 1
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))

    # Listing files at server
    fileList = clientSocket.recv(4096)
    decodedFileList = fileList.decode()
    print("Available files at server:")
    print(decodedFileList)

    # while flag == 1:
    # Ask Client Upload/Download
    userRequest = input("To Download file--> press 'download', To upload file---> press 'upload':", )
    clientSocket.send(userRequest.encode())
    print(userRequest)

    if userRequest == 'download':
        fileName = input("file Name?:")
        fileNameEncoded = fileName.encode()
        clientSocket.send(fileNameEncoded)
        print("make sure of filename:", fileNameEncoded)

        if fileNameEncoded != b'q':
            # clientSocket.send(bytes_text)
            data = clientSocket.recv(1024)
            data = data.decode()
            print("server replay:", repr(data[6:]))

            if data[:6] == "Exists":
                filesize = (data[6:])
                message = input("file Exists," + str(filesize) + "Bytes,download?(Y/N)?->")
                if message == 'Y':
                    clientSocket.send('OK'.encode())
                    f = open('new' + fileName, 'wb')
                    data = clientSocket.recv(1024)
                    f.write(data)
                    totalrecv = len(data)
                    print("received data:", data)
                    print("total received data:", totalrecv)
                    print("file size:", filesize)

                    while totalrecv < int(filesize):
                        data = clientSocket.recv(1024)
                        totalrecv += len(data)
                        f.write(data)
                        # print("{0:.2f}".format((totalrecv / float(filesize))) * 100 + \
                        #       "%Done")
                        print(data, " ")
                    print("Download complete")
                    f.close()
            else:
                print("file doesn't exist")
    elif userRequest == 'upload':
        fileName = input("file Name?:")
        fileNameEncoded = fileName.encode()
        clientSocket.send(fileNameEncoded)
        clientSocket.send(("file size is:" + str(os.path.getsize(fileNameEncoded))).encode())
        print("->Yarab", str(os.path.getsize(fileNameEncoded)).encode())

        if fileNameEncoded != b'q':
            # take confirmation from server 'OK'

            server_replay = clientSocket.recv(1024)
            server_replay_decoded = server_replay.decode()
            print("------>", server_replay_decoded)
            if server_replay_decoded == 'OK':
                print("Entered")
                with open(fileNameEncoded, 'rb') as f:
                    bytesToSend = f.read(1024)
                    clientSocket.send(bytesToSend)
                    while bytesToSend != "":
                        bytesToSend = f.read(1024)
                        clientSocket.send(bytesToSend)
                f.close()
                print("finished")
            else:
                clientSocket.send(b"ERROR")
        # ask the client whether he wants to continue
        # ans = input('\nDo you want to continue(y/n) :')
        # if ans == 'y':
        #     flag = 1
        # else:
        #     flag = 0
    clientSocket.close()


if __name__ == '__main__':
    main()
