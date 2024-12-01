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


def getAllBrandsFromDB():
    """
    Fetch all brands from the database.
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
            # Fetch all brands from the Brands table
            cursor.execute("SELECT * FROM Brands")
            brands = cursor.fetchall()

            return brands

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        raise
