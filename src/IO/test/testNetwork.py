
# Import general packages
from __future__ import absolute_import
import sys

# Import project files
from IO.network import *

def main():
    mode = sys.argv[1]
    port = 21 # Port 21 is the default FTP port
    timeout = 5

    print("Network Test Started")

    while True:
        if mode == "server":
            print("Broadcasting")
            data, address = network.broadcastMessageAndWaitForResponse(port, "Server Broadcast Test", timeout)
            if data == "Client Response Test":
                print(f"Client Responded from {address}. Attempting Socket Connection")
                connection = network.establishConnection(address[0], port)

                if network.checkIfConnected(connection):
                    print("Connected to Client. Sending Server Test Message")
                    network.sendString(connection, "Server Socket Test")
                    data = network.receiveString(connection)
                    if data == "Client Socket Test":
                        print("Client Socket Test Successful")
                        connection.close()
                        network.broadcastMessage(port, "Server Broadcast Test Complete")
                        break
                    else:
                        print("Client failed to respond")
                else:
                    print("Socket Connection Failed")
            else:
                print("No Response")
        elif mode == "client":
            print("Waiting for Broadcast")
            data, address = network.waitForMessage(port, timeout)
            if data == "Server Broadcast Test":
                print(f"Server Responded from {address}. Attempting Socket Connection")
                connection = network.establishConnection(address[0], port)

                if network.checkIfConnected(connection):
                    print("Connected to Server. Sending Client Test Message")
                    network.sendString(connection, "Client Socket Test")
                    data = network.receiveString(connection)
                    if data == "Server Socket Test":
                        print("Server Socket Test Successful")
                        connection.close()
                        network.broadcastMessage(port, "Client Response Test")
                        break
                    else:
                        print("Server failed to respond")
                else:
                    print("Socket Connection Failed")
            else:
                print("No Response")


# Run the program
if __name__ == '__main__':
    main()
