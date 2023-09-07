
import socket
import sys

def broadcastMessageAndWaitForResponse(port, msg, waitTime):
    broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcaster.bind(('', 0))
    broadcaster.settimeout(waitTime)
    broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # convert msg to bytes
    broadcaster.sendto(msg.encode(), ('<broadcast>', port))

    ret = (None, None)
    try:
        data, address = broadcaster.recvfrom(1024)
        data = data.decode()
        ret = (data, address)
    except socket.timeout:
        pass
    broadcaster.close()
    return ret

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

def broadcastMessage(port, msg):
    broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcaster.bind(('', 0))
    broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcaster.sendto(msg, ('<broadcast>', port))
    broadcaster.close()

def establishConnection(host, port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((host, port))
    return connection

def sendString(connection, string):
    connection.sendall(string.encode())

def receiveString(connection):
    return connection.recv(1024).decode()

def checkIfConnected(connection):
    try:
        connection.sendall("".encode())
        return True
    except:
        return False

# I really wanted this to be in it's own test file but Python relative importing sucks.
def _test():
    mode = sys.argv[1]
    port = 21 # Port 21 is the default FTP port
    timeout = 5

    print("Network Test Started")

    while True:
        if mode == "server":
            print("Broadcasting")
            data, address = broadcastMessageAndWaitForResponse(port, "Server Broadcast Test", timeout)
            if data == "Client Response Test":
                print(f"Client Responded from {address}. Attempting Socket Connection")
                connection = establishConnection(address[0], port)

                if checkIfConnected(connection):
                    print("Connected to Client. Sending Server Test Message")
                    sendString(connection, "Server Socket Test")
                    data = receiveString(connection)
                    if data == "Client Socket Test":
                        print("Client Socket Test Successful")
                        connection.close()
                        broadcastMessage(port, "Server Broadcast Test Complete")
                        break
                    else:
                        print("Client failed to respond")
                else:
                    print("Socket Connection Failed")
            else:
                print("No Response")
        elif mode == "client":
            print("Waiting for Broadcast")
            data, address = waitForMessage(port, timeout)
            if data == "Server Broadcast Test":
                print(f"Server Responded from {address}. Attempting Socket Connection")
                connection = establishConnection(address[0], port)

                if checkIfConnected(connection):
                    print("Connected to Server. Sending Client Test Message")
                    sendString(connection, "Client Socket Test")
                    data = receiveString(connection)
                    if data == "Server Socket Test":
                        print("Server Socket Test Successful")
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
