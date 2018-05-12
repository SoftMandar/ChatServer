import argparse

from scripts.config import *
from scripts.database.database_manager import DatabaseManager
#from scripts.server.chat_server import ChatServer

argument_parser = argparse.ArgumentParser(description="Command line commands for manipulating the chat server")

argument_parser.add_argument('-d' ,'--init-database', dest="database" ,help="Initialize database")
argument_parser.add_argument('-s' ,'--start-server', dest="server",help="Start server process")

args = argument_parser.parse_args()

with DatabaseManager(DATABASE_CONFIG) as db_test:
    #db_test.add_table_entry("player", name="Rares", password="loooo")
    db_test.get_table_by_name("player", "Rares", "name", "password)
"""if args.database:
        init_database()
else:
    chat_serv = ChatServer()
    chat_serv.start_server()
"""
