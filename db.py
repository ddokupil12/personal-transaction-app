from contextlib import contextmanager
from mysql.connector import Error, connect

from context import DB_CONFIG

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
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

def db_fetchall(*args):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        if len(args) == 1:
            query = args[0]
            cursor.execute(query)
        elif len(args) == 2:
            query = args[0]
            dbArgs = args[1]
            cursor.execute(query, dbArgs)
        else:
            raise ValueError("Can't accept multiple queries or arguments")
        
        return cursor.fetchall()
    

def db_fetchone(*args):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        if len(args) == 1:
            query = args[0]
            cursor.execute(query)
        elif len(args) == 2:
            query = args[0]
            dbArgs = args[1]
            cursor.execute(query, dbArgs)
        else:
            raise ValueError("Can't accept multiple queries")
        
        return cursor.fetchone()
    

def db_commit(*args):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        lenArgs = len(args)
        if lenArgs % 2 == 0:
            for i in range(0, lenArgs, 2):
                query = args[i]
                dbArgs = args[i + 1]
                cursor.execute(query, dbArgs)
        else:
            raise ValueError("Expected an even number of arguments")
        
        conn.commit()