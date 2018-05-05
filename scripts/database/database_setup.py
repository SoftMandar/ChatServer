import logging
from collections import OrderedDict

import mysql.connector as mysql
from mysql.connector import errorcode

from scripts.config import *

logger = logging.getLogger(__name__ + ".database_setup")

database_entries = OrderedDict()

database_entries['database'] = "CREATE DATABASE chat_db;"
database_entries['player'] = ("CREATE TABLE player ("
"id int(11) PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL,"
"username varchar(255) UNIQUE NOT NULL,"
"password varchar(255) NOT NULL"
"last_join datetime"
");")
database_entries['channel'] = ("CREATE TABLE channel("
"id int(11) PRIMARY KEY AUTO_INCREMENT UNIQUE NOT NULL,"
"pid int(11),"
"channel_name varchar(255) UNIQUE NOT NULL,"
"password varchar(255),"
"FOREIGN KEY (pid) REFERENCES player(pid)"
");")


def init_database():

    global database_entries

    try:
        database_connection = mysql.connect(**DATABASE_CONFIG)
    except mysql.Error as merr:
        if merr.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error("Access denied")
        elif merr.errno == errorcode.ER_BAD_DB_ERROR:
            database_cursor = database_connection.cursor()
            for entries in database_entries:
                database_cursor.execute(entries)
            logger.info("Database finally initialized")
    else:
            logger.info("Database already initialized")
