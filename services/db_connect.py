import mysql.connector

__db=None

def connect():
    global __db
    if __db==None:
        __db=mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='123456',
            database='grocery_app'
        )
    return __db

