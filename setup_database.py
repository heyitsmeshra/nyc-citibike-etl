import psycopg2

from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def execute_sql_file(cursor,file_path):

    with open(file_path,"r") as file:
        cursor.execute(file.read())


def main():

    connection=None
    cursor=None

    try:

        connection=psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor=connection.cursor()

        sql_files=[
            "sql/create_tables.sql",
            "sql/indexes.sql",
            "sql/views.sql"
        ]

        for sql_file in sql_files:
            execute_sql_file(cursor,sql_file)

        connection.commit()

        print("Database setup completed successfully.")

    except psycopg2.Error as e:

        print(f"Database setup failed: {e}")

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


if __name__=="__main__":
    main()