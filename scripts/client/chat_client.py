import socket
import sys
import select
import datetime

from profanityf.profanity import ProfanityFilter
class ClientChat(object):

    MAX_RECV_BYTES = 1024

    def __init__(self, server_address, profanity=True):

        self.prof_filter = ProfanityFilter() if profanity else None

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Trying to connect to {}... ".format(server_address[0], server_address[1]))
        try:
            self.client_socket.connect(server_address)
        except socket.error as serr:
            print("Failed to connect to server")
            sys.exit(1)
        else:
            print("Client connected ... ")

        self.inputs = [ sys.stdin , self.client_socket ]

    def send_message(self, message):

        clean_message = self.prof_filter.replace_text(message)
        try:
            self.client_socket.send(clean_message.encode("utf-8"))
        except IOError as ierr:
            print("Error on sending data...")
            sys.exit(1)

    def recv_message(self, sock):
        try:
            recv_message = sock.recv(ClientChat.MAX_RECV_BYTES)
        except IOError as ierr:
            sys.exit(1)
        else:
            return recv_message.decode("utf-8")

    def connect_forever(self):

        while True:
            try:
                readable, writeable, exception = select.select(self.inputs, [], [])
                for sock in readable:
                    if sock == self.client_socket:
                        message = self.recv_message(sock)
                        print("[{}]: {}".format(datetime.datetime.now(),message))

                    else:
                        message = sys.stdin.readline()
                        self.send_message(message)
            except KeyboardInterrupt as kerr:
                self.client_socket.close()
                sys.exit(0)
    def send_whisper(self, client, message):
        pass

clt_obj = ClientChat(("127.0.0.1", 8080))

clt_obj.connect_forever()
