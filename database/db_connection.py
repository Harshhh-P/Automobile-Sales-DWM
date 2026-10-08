import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False
    )

    return connection


if __name__ == "__main__":
    try:
        connection = get_connection()

        if connection.is_connected():
            print("Successfully connected to Aiven MySQL!")

            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")

            database = cursor.fetchone()
            print("Connected Database:", database[0])

            cursor.close()
            connection.close()

            print("Connection closed successfully.")

    except mysql.connector.Error as error:
        print("Database connection failed!")
        print("Error:", error)