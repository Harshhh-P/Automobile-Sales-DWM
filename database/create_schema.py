from db_connection import get_connection


def create_schema():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        with open("database/schema.sql", "r", encoding="utf-8") as file:
            sql_script = file.read()

        statements = sql_script.split(";")

        for statement in statements:
            statement = statement.strip()

            if statement:
                cursor.execute(statement)

        connection.commit()

        print("========================================")
        print("Aiven database schema created successfully!")
        print("========================================")

    except Exception as error:
        print("Schema creation failed!")
        print("Error:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


if __name__ == "__main__":
    create_schema()