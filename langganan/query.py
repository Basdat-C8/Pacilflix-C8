import psycopg2
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def create_connection():
    try:
        connection = psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        with connection.cursor() as cursor:
            cursor.execute("SET search_path TO Pacilflix;")
        return connection
    except Exception as e:
        logger.error("Error in connecting to the database: %s", e)
        return None
    
# =================================================

def query_get_transaksi(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM transaction WHERE username='{username}';")
    return cursor.fetchall()