__all__ = ['get_db_connection', 'db_fetchall', 'db_fetchone', 'db_commit']

from contextlib import contextmanager
from mysql.connector import Error, connect

from app import DB_CONFIG

@contextmanager
def get_db_connection():
    # Context manager for database connections
    connection = None
    try:
        connection = connect(**DB_CONFIG)
        yield connection
    except Error as e:
        print(f'Error connecting to MySQL: {e}')
        if connection:
            connection.rollback()
        raise Exception(e)
    finally:
        if connection and connection.is_connected():
            connection.close()

def _db_fetch(*args, all=True):
    # Fetch queries from the database
    #
    # Fetch one row or all rows from the database connected to the server.
    # 
    # :param all: bool (True: returns all rows | False: returns one)
    # :param args: str[, tuple] (The first argument is the query,
    #     and the second argument is the arguments for that query)

    # Returns:
    # All matching rows (when all=True)
    # One matching row (when all=False)

    # Raises:
    # ValueError when there are more than two arguments
    # """
    lenArgs = len(args)
    if lenArgs > 2:
        raise ValueError("Can't accept multiple queries")
    
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        query = args[0]
        if lenArgs == 1:
            cursor.execute(query)
        elif lenArgs == 2:
            dbArgs = args[1]
            cursor.execute(query, dbArgs)

        if all:
            return cursor.fetchall()
        else:
            return cursor.fetchone()

def db_fetchall(*args): return _db_fetch(*args, all=True)
    
def db_fetchone(*args): return  _db_fetch(*args, all=False)
    
def db_commit(*args):
    # Docstring for db_commit
    
    # :param args: an even list of arguments of queries followed by
    #     the arguments for those queries.
    #     query1, dbArgs1[, query2, dbArgs2] ...

    # Raises:
    # ValueError when there aren't any, or an even number of, arguments
    lenArgs = len(args)
    if lenArgs == 0:
        raise ValueError("Expected at least 2 arguments")
    elif lenArgs % 2 != 0:
        raise ValueError("Expected an even number of arguments")
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        lenArgs = len(args)
        for i in range(0, lenArgs, 2):
            query = args[i]
            dbArgs = args[i + 1]
            cursor.execute(query, dbArgs)

        conn.commit()