import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch database credentials from environment variables

# Fetch database credentials from environment variables
ENDPOINT = os.getenv("ENDPOINT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")


def getGenerationsByBrand(brand_id):
    """
    Fetch all generations associated with a specific brand.

    Args:
        brand_id (int): ID of the brand.

    Returns:
        list: List of generations associated with the brand.
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
            # SQL query to fetch generations by brand ID
            sql = """
                SELECT generation_id, generation_data
                FROM generations
                WHERE brand_id = %s
            """
            cursor.execute(sql, (brand_id,))
            generations = cursor.fetchall()

            return generations

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        raise
