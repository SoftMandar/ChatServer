import logging
import sys

import mysql.connector as mysql
from mysql.connector import errorcode

from ..exceptions.base_exceptions import *

class DatabaseManager(object):

    def __init__(self, database_config):

        self.database_logger = logging.getLogger(__name__ + ".database_log")
        self.database_config = database_config

    def __enter__(self):
        try:
            self.db_connection = mysql.connect(**self.database_config)
        except mysql.Error as merr:

            if merr.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.database_logger.exception("Access denied")
            else:
                self.database_logger.exception(merr)

        self.cursor = self.db_connection.cursor()
        return self

    def __exit__(self, *args, **kwargs):
        self.cursor.close()
        self.db_connection.close()

    def __repr__(self):

        return "Class: <{}>".format(self.__name__)

    def add_table_entry(self, table, **kwargs):
        query = [ "INSERT INTO %s " % table ]

        if kwargs:
            query.append("(%s)" % ','.join(["%s" % e for e in \
                                list(kwargs.keys())]))
            query.append(" VALUES (%s);" % ','.join(["'%s'" % e for e in \
                                list(kwargs.values())]))
        try:
            self.cursor.execute(''.join(query))
            self.db_connection.commit()
        except mysql.Error as merr:
            if merr.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                self.database_logger.exception("Table dosen't exist")
            else:
                self.database_logger.exception(merr)

    def get_table_entry(self, table, **kwargs):
        query = ""

        if kwargs:
            query % "SELECT %s FROM %s" % (",".join(["%s" % q for q in \
                                        list(kwargs.keys())]), table)
        try:
            self.cursor.execute("".join(query))
        except mysql.Error as merr:
            if merr.errno == errorcode.ER_TABLE_EXIST_ERROR:
                self.database_logger.exception("Table dosen't exist")
            else:
                self.database_logger.exception(merr)

    def get_table_by_name(self, table, name ,*args):

        query = "SELECT %s FROM %s WHERE %s"

        if args:
            query = query % (",".join([q for q in args]), table, "name='%s'" % name)
        try:
            self.cursor.execute(query)
        except mysql.Error as merr:
            if merr.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                self.database_logger.exception("Table dosen't exist")
            else:
                self.database_logger.exception(merr)
        player = self.cursor.fetchone()
        if player is not None:
            return player
        else:
            raise PlayerNotFoundException("Player dosen't exists in database entry")
