import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch database credentials from environment variables
ENDPOINT = os.getenv("ENDPOINT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")


def createBrandInDB(brand_name, brand_type, description, color_scheme):
    """
    Insert a new brand into the Brands table.
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
    try:
        with connection.cursor() as cursor:
            # Insert a new brand into the Brands table
            cursor.execute(
                """
                INSERT INTO Brands (brand_name, type, description, color_scheme)
                VALUES (%s, %s, %s, %s)
                """,
                (brand_name, brand_type, description, color_scheme),
            )

            # Commit the transaction
            connection.commit()

            print(f"Brand '{brand_name}' successfully created.")

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        raise
