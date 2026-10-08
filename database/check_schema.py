from db_connection import get_connection


try:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES;")

    print("\nTables in Aiven database:")
    print("-" * 40)

    for table in cursor.fetchall():
        print(table[0])

    cursor.close()
    connection.close()

except Exception as error:
    print("Error:", error)