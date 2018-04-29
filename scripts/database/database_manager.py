import logging
import sys

import mysql.connector as mysql
from mysql.connector import errorcode

class DatabaseManager(object):

    def __init__(self, database_config):

        self.database_config = database_config

    def __enter__(self):
        try:
            self.db_connection = mysql.connect(**self.database_config)
        except mysql.Error as merr:

            if merr.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                pass
            elif merr.errno == errorcode.ER_BAD_DB_ERROR:
                pass
            else:
                pass
        self.cursor = self.db_connection.cursor()
        return self

    def __exit__(self):

        self.cursor.close()
        self.db_connection.close()

    def __repr__(self):

        return "Class: <{}>".format(self.__name__)

    def add_table_entry(self, table, **kwargs):

        query = [ "INSERT INTO %s " % table ]

        if kwargs:
            query.append("%s" % ','.join(["%s" % e for e in \
                                list(kwargs.keys())]))
            query.append("VALUES (%s)" % ','.join(["'%s'" % e for e in \
                                list(kwargs.values())]))
        try:
            self.cursor.execute(''.join(query))
        except mysql.Error as merr:
            if merr.errno == errorcode.ER_TABLE_EXIST_ERROR:
                pass


    def get_table_entry(self, table, **kwargs):
        query = []

        if kwargs:
            query.append( "SELECT %s FROM" % )

        try:
            self.cursor.execute()
        except mysql.Error as merr:
            if merr.errno == errorcode.ER_TABLE_EXIST_ERROR:
                pass
        else:
            pass
