
import socket
import sys


def waitForMessage(port, waitTime):
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.bind(('', port))
    listener.settimeout(waitTime)
    ret = (None, None)
    try:
        data, address = listener.recvfrom(1024)
        data = data.decode()
        ret = (data, address)
    except socket.timeout:
        pass
    listener.close()
    return ret

def waitForSocketConnection(port, waitTime):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(('', port))
    listener.settimeout(waitTime)
    ret = None
    try:
        listener.listen(1)
        ret = listener.accept()
    except socket.timeout:
        pass
    except KeyboardInterrupt:
        exit()
    return ret

def broadcastMessage(port, msg):
    broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcaster.bind(('', 0))
    broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcaster.sendto(msg.encode(), ('<broadcast>', port))
    broadcaster.close()

def requestConnection(host, port, timeout):
    socket.setdefaulttimeout(timeout)
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection

def sendString(connection, string):
    connection.sendall(string.encode())

def receiveString(connection):
    return connection.recv(1024).decode()

# I really wanted this to be in it's own test file but Python hates relative importing.
def _test():
    mode = sys.argv[1]
    port = 21 # Port 21 is the default FTP port
    timeout = 5

    print("Network Test Started")

    while True:
        if mode == "server":
            print("Broadcasting")
            broadcastMessage(port, "Server Broadcast Test")
            connection = waitForSocketConnection(port, timeout)
            if connection is not None:
                client_socket, client_address = connection
                print(f"Connected to Client {connection}. Sending Server Test Message")
                sendString(client_socket, "Server Socket Test")
                data = receiveString(client_socket)
                if data == "Client Socket Test":
                    print(f"Received {data}. Client Socket Test Successful")
                    client_socket.close()
                    broadcastMessage(port, "Server Broadcast Test Complete")
                    break
                else:
                    print("Client failed to respond")
            else:
                print("No Response")
        elif mode == "client":
            print("Waiting for Broadcast")
            data, address = waitForMessage(port, timeout)
            if data == "Server Broadcast Test":
                print(f"Server Responded from {address}. Attempting Socket Connection")
                connection = requestConnection(address[0], port, timeout)
                if connection is not None:
                    print(f"Connected to Server {connection}. Sending Client Test Message")
                    sendString(connection, "Client Socket Test")
                    data = receiveString(connection)
                    if data == "Server Socket Test":
                        print(f"Received {data}. Server Socket Test Successful")
                        connection.close()
                        broadcastMessage(port, "Client Response Test")
                        break
                    else:
                        print("Server failed to respond")
                else:
                    print("Socket Connection Failed")
            else:
                print("No Response")


# Run the program
if __name__ == '__main__':
    _test()
