"""
In this file, an abstract database class is defined, so other classes can inherit from this class for a connection to
the database file. There can be different purposes for a database connection.
"""

import sqlite3


class MasterDatabaseClass:
    """
    Create an abstract/master database class with access to the database file.
    """
    def __init__(self):
        # Initialize a connection and if this file does not exist, it is created in this step. The isolation level is
        # set to None, so autocommit is possible.
        database_connection = sqlite3.connect("pokemon.db", isolation_level=None)

        # Use a cursor as class object, so every function has access to the database.
        self.database_cursor = database_connection.cursor()
