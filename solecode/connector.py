from unittest import result
import mysql.connector
import pymysql

# Connect DB Parkiran

def openDb():
    db = pymysql.connect(
        host = "localhost",
        user = "root",
        database = "parkir",
    )
    
    return db