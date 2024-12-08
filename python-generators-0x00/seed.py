#!/usr/bin/env python3

import csv

import mysql.connector


# connects to the mysql database server
def connect_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
    )
    return db


# connects the the ALX_psrodev database in MYSQL✅
def connect_to_prodev():
    ALX_prodev_db = mysql.connector.connect(
        host="localhost", user="root", password="", database="ALX_prodev"
    )
    return ALX_prodev_db


# creates the database ALX_prodev if it does not exist✅
def create_database(connection):
    curs = connection.cursor()
    curs.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    curs.close()
    connection.commit()
    return


# creates a table user_data if it does not exists with the required fields✅
def create_table(connection):
    curs = connection.cursor()
    curs.execute(
        """
                 CREATE TABLE IF NOT EXISTS user_data (
                     user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                     name VARCHAR(255) NOT NULL, 
                     email VARCHAR(255) NOT NULL,
                     age DECIMAL(3,0) NOT NULL,
                     INDEX (user_id)
                     );
      """
    )
    curs.close()
    connection.commit()
    return


# inserts data in the database if it does not exist
def insert_data(connection, data):
    cursor = connection.cursor()

    with open(data, "r") as f:
        reader = csv.reader(f)

        next(reader)  # Skip the first row (header)

        for row in reader:
            # Convert the age (3rd column) to a decimal
            row[2] = float(row[2])

            cursor.execute(
                "INSERT INTO user_data (name, email, age) VALUES (%s, %s, %s)",
                row,
            )
    cursor.close()
    connection.commit()
    return


# db = connect_db()
# print(f"Connected to {db}")

# create_database(db)

# Alx_prodev_db = connect_to_prodev()
# print(f"Connectfded to {Alx_prodev_db}")

# create_table(Alx_prodev_db)

# insert_data(Alx_prodev_db, "user_data.csv")
