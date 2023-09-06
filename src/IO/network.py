
import socket

def broadcastMessageAndWaitForResponse(port, msg, waitTime):
    broadcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcaster.bind(('', 0))
    broadcaster.settimeout(waitTime)
    broadcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcaster.sendto(msg, ('<broadcast>', port))

    ret = None
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
    ret = None
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
