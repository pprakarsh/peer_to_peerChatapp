import socket
import select
import sys


def chat(sock):
    
    inputs = [sock, sys.stdin]
    #chat starts
    while True:
        readers, _, _ = select.select([sock, sys.stdin], [], [])
        msg = ""
        for reader in readers:
            if reader is sock:
                msg = sock.recv(BUFSIZE).decode('utf8')
                if msg != "!q":
                    print(f"<<Friend>> {msg}")
                else:
                    print(f"Friend closed connection")
                    sock.close()
            else:
                msg = sys.stdin.readline().rstrip()
                if msg != "!q":
                    print(f"<<Me>> {msg}")
                    sock.send(bytes(msg, 'utf-8'))
                else:
                    sock.send(bytes(msg, 'utf-8'))
                    print(f"Closing connection")
                    sock.close()

            if msg == "!q":
                break

        if msg == "!q":
            break


BUFSIZE = 1024
if __name__ == "__main__":
    PORT1 = int(input("Please enter Port Number1 ")) 
    PORT2 = int(input("Please enter Port Number2 ")) 
    HOST = ''
    ADDR1 = (HOST, PORT1)
    ADDR2 = (HOST, PORT2)

    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(ADDR1)
    listen_sock.listen(5)
    
    print("Waiting for connection ....")
    
    inputs = [listen_sock, sys.stdin]
    while True:
        app = ""
        readers, _, _ = select.select(inputs, [], [])
        for reader in readers:
            if reader is listen_sock:
                print("I am listen_socket")
                chat_sock_serv, client_addr = listen_sock.accept()
                app = "server"
                break
            else:
                print("I am stdin")
                chat_sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                chat_sock_client.connect(ADDR2)
                app = "client"
                break

        if app == "server":
            chat(chat_sock_serv)
            del chat_sock_serv
        elif app == "client":
            chat(chat_sock_client)
            del chat_sock_client
    
