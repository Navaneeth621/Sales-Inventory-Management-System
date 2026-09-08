import os

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_connection():

    try:

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),

            # Use pure Python implementation.
            # This avoids the mysql_native_password
            # concurrent connection issue with the C extension.
            use_pure=True
        )

        if connection.is_connected():

            return connection

    except Error as e:

        print("Database connection failed.")
        print("Error:", e)

    return None


# ============================================================
# TEST DATABASE CONNECTION
# ============================================================

if __name__ == "__main__":

    connection = create_connection()

    if connection:

        print("MySQL connection successful.")

        connection.close()

    else:

        print("MySQL connection failed.")