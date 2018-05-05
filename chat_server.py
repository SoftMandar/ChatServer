import argparse

from scripts.database.database_setup import init_database
from scripts.server.chat_server import ChatServer

argument_parser = argparse.ArgumentParser(description="Command line commands for manipulating the chat server")

argument_parser.add_argument('-d' ,'--init-database', dest="database" ,help="Initialize database")
argument_parser.add_argument('-s' ,'--start-server', dest="server",help="Start server process")

args = argument_parser.parse_args()

if args.database:
        init_database()
else:
    chat_serv = ChatServer()
    chat_serv.start_server()
