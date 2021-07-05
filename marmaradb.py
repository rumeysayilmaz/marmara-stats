import os, json
import os.path
from mysql.connector import connect, Error
import mysql.connector
import re


def get_db_credentials():
    current_dir = os.getcwd()
    db_config_file = current_dir + '/db.conf'
    with open(db_config_file, 'r') as f:
        for line in f:
            l = line.rstrip()
            if re.search('host', l):
                host = l.replace('host=', '')
            elif re.search('user', l):
                username = l.replace('user=', '')
            elif re.search('password', l):
                password = l.replace('password=', '')
            elif re.search('database', l):
                database = l.replace('database=', '')
    return host, username, password, database


def db_connection():
    try:
        db_credentials = get_db_credentials()
        hostname = db_credentials[0]
        username = db_credentials[1]
        db_password = db_credentials[2]
        db = db_credentials[3]
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=db_password,
            database=db,
        )
        print(connection)
        return connection
    except Error as e:
        print(e, 'error')


def read_record(sql_statement):
    try:
        connection = db_connection()  # make a db connection
        cursor = connection.cursor()  # create a cursor for the db_connection
        cursor.execute(sql_statement)  # execute the sql_statement
        records = cursor.fetchall()  # fetches all rows from the last executed statement i.e. sql_statement
        return records, connection, cursor
    except mysql.connector.Error as e:
        print("Error reading records from MySQL table", e)


def close_connection(connection, cursor):
    if connection.is_connected():
        connection.close()
        cursor.close()
        print("MySQL connection is closed")


def insert_record(sql_statement):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    connection.commit()


def insert_record_set(query, record_list):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute(query, record_list)
    connection.commit()
