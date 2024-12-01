import pymysql
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Fetch database credentials from environment variables
ENDPOINT = os.getenv("ENDPOINT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")


def insertGenerationData(brand_id, generation_data):
    """
    Insert a new generation record into the generations table.

    Args:
        brand_id (int): ID of the brand associated with this generation.
        generation_data (dict): JSON data to insert into the table.

    Returns:
        int: ID of the newly inserted record.
    """
    connection = pymysql.connect(
        host=ENDPOINT,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        port=PORT,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    generation_data = json.dumps(generation_data)
    try:
        with connection.cursor() as cursor:
            # SQL query to insert data
            sql = """
                INSERT INTO generations (brand_id, generation_data)
                VALUES (%s, %s)
            """
            # Execute the query
            cursor.execute(sql, (brand_id, generation_data))

            # Commit the transaction
            connection.commit()

            # Return the ID of the newly inserted record
            return cursor.lastrowid

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        raise
