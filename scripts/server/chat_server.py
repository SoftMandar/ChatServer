import socket
import select
import sys

try:
    import queue
except ImportError:
    import Queue as queue

from ..config import *
from ..database.database_manager import DatabaseManager

class ChatServer(object):

    def __init__(self, server_address=None, reuse_addr=True, back_log=10,
                    blocking_mode=False):
        """
            ChatServer - class

            Positional Arguments: None


            KeyWordArguments:
                --server_address: Initial set to None ,will be set from the config
                file , else it will be set with the desired address.

                --reuse_addr: Used to indicate if the service will have a static
                reusable address everytime will start.

                --bacl_log: Used parameter for listen , indicates the maximum
                number of clients in the session queue.
                --blocking_mode: Will set the socket as blocking or nonblocking.

                --cfg_file: Default file for server configuration

            We have more options of configurations:
                -- Class
                -- Dict
                -- File config
                -- Mixing
            config_parser

            Arguments:

            --cfg_file: file configuration path
        """

        self.__server_logger = logging.getLogger(__name__ + ".chat_server")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue= {}

        if server_address is not None:
            self.server_address = server_address
        else:
            self.server_address = (str(config_parser.get("server_config", "host_address")),
                int(config_parser.get("server_config", "port")))
        try:
            self.server_socket.bind(self.server_address)
        except socket.error as serr:
            self.__server_logger.exception("Error binding socket")
            sys.exit(1)

        if reuse_addr:
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        if blocking_mode:
            self.server_socket.setblocking(1)

        self.server_socket.listen(back_log)

        self.__server_logger.info("[ SERVER ] started listen on ({}:{})".format(self.server_address[0],
                    self.server_address[1]))
        self.server_status = True

        self.inputs = inputs = [ self.server_socket]

        self.outputs = []

        self.clients_connected = {}

    def start_server(self):

        try:
            while self.server_status:
                # Monitorize client sock (file descriptor)
                readable, writeable, exceptional = select.select(self.inputs, self.outputs, self.inputs)

                for sock in readable:

                    if sock is self.server_socket:
                        client_sock, client_addr = self.server_socket.accept()
                        self.__server_logger.info("[ CLIENT ] Client just connected with address {}:{}".format(
                                client_addr[0],client_addr[1]
                        ))
                        client_sock.setblocking(0)
                        self.inputs.append(client_sock)

                        self.message_queue[client_sock] = queue.Queue()
                    else:
                            self.handle_client(sock)
                for sock in writeable:

                    #Try to extract message from msg_queue
                    try:
                        message = self.message_queue[sock].get_nowait()
                    except queue.Empty as qerr:
                        self.__server_logger.exception("Error queue for client is empty")
                        sys.exit(1)
                    else:
                        for client in self.inputs[1:]:
                            self.send_message(client, message)

                for sock in exceptional:
                    self.__server_logger.exception("Client just encountered error")
                    self.inputs.remove(sock)
                    if sock in self.outputs:
                        self.outputs.remove(sock)

                    del self.message_queue[sock]
                    sock.close()

        except KeyboardInterrupt as kerr:
            self.shutdown_server()

    def shutdown_server(self):
        self.__server_logger.info("Server is closing...")
        for client in self.inputs:
            self.disconnect_client(client)
        self.server_status = False
        self.server_socket.close()
        sys.exit(0)

    def send_message(self,client_sock, message):

        try:
            client_sock.send(message)
        except IOError as ioerr:
            self.__server_logger.exception("Error on sending to client")
            sys.exit(1)
        else:
            if client_sock in self.outputs:
                self.outputs.remove(client_sock)

    def recieve_whisper(self, client, message):
        pass

    def handle_client(self, client_socket):

        MAX_RECV_BYTES = 1024

        data_buffer = ""

        try:
            data_buffer = client_socket.recv(MAX_RECV_BYTES)
        except IOError as ierr:
            self.__server_logger.error(str(ierr))
            sys.exit(1)

        else:
            if not data_buffer:
                self.disconnect_client(client_socket)
            else:
                data_unpacked = command.decode("utf-8")
                command = data_buffer.split(" ")[0]
                if command[1] == "w":

                elif command[1] == "p":

                self.message_queue[client_socket].put(data_buffer)
                if client_socket not in self.outputs:
                    self.outputs.append(client_socket)

    def disconnect_client(self, client_socket):
        self.__server_logger.info("Client just disconnected")
        self.inputs.remove(client_socket)
        if client_socket in self.outputs:
            self.outputs.remove(client_socket)
        if  lient_socket in list(self.message_queue.keys()):
            del self.message_queue[client_socket]
        cli.split(" ")
        nt_socket.close[0]()
