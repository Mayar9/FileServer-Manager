import os
import socket
import threading


def uploadFile(name, connection):
    filename = connection.recv(1024)
    total_size: str = connection.recv(1024)
    print("lect",total_size)
    size = total_size[13:]
    file_name_encoded = filename.decode()
    print(file_name_encoded)

    if file_name_encoded != b'':
        connection.send('OK'.encode())

        f = open('new' + file_name_encoded, 'wb')
        data = connection.recv(1024)
        f.write(data)
        total_recv = len(data)
        # file_size = (data[0:])
        # print(file_size)
        print("received data:", data)
        print("total received data:", total_recv)
        print(int(size))

        while total_recv < int(size):
            print("entered")
            data = connection.recv(1024)
            total_recv += len(data)
            f.write(data)
            print(data, " ")
        print("upload complete")
        f.close()
    else:
        print("Error")
        connection.close()


def RetrFile(sock):
    filename = sock.recv(1024)
    fileNameEncoded = filename.decode()
    # print(data)

    # check Existence of file
    if os.path.isfile(fileNameEncoded):
        sock.send(("Exists" + " " + str(os.path.getsize(fileNameEncoded))).encode())
        print("success")
        userResponse = sock.recv(1024)
        userResponse.decode()
        print("userResponse is:", userResponse[0:4])

        if userResponse[0:4] == b'OK':
            with open(fileNameEncoded, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
        else:
            sock.send(b"ERROR")
    else:
        print("file Not Exist")
        sock.close()


def main():
    host = '127.0.0.1'
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print("server started ..... Listening for new connection")

    # conn, address = s.accept()
    # print("client connected IP: <" + str(address) + ">")

    while True:
        conn, address = s.accept()
        print("client connected IP: <" + str(address) + ">")

        # Listing Files in Server
        filelist = str(os.listdir())
        fileListEncoded = filelist.encode()
        conn.send(fileListEncoded)
        # print(fileListEncoded)

        # Request: Download or Upload
        receivedRequest = conn.recv(1024)
        print("clientRequest:", receivedRequest.decode())

        if receivedRequest == b'download':
            t = threading.Thread(target=RetrFile, args=(conn,))
            t.start()
        elif receivedRequest == b'upload':
            t = threading.Thread(target=uploadFile, args=("uploadThread", conn))
            t.start()

    s.close()


if __name__ == '__main__':
    main()
