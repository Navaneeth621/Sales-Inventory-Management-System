import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def create_connection():

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print("Database connection failed.")
        print("Error:", e)

    return None


if __name__ == "__main__":
    connection = create_connection()

    if connection:
        print("MySQL connection successful.")
        connection.close()
    else:
        print("MySQL connection failed.")