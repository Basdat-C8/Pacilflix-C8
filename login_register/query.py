import psycopg2
from django.conf import settings
from psycopg2.extras import RealDictCursor
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

def register_user(username, password, country):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            hashed_password = password  # Here, you should implement actual password hashing
            query = "INSERT INTO pengguna (username, password, negara_asal) VALUES (%s, %s, %s);"
            cursor.execute(query, (username, hashed_password, country))
            conn.commit()
            return True  # Ensure this is reached on success
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("Error in register_user: %s", error)
            return False  # Properly handling errors
        finally:
            cursor.close()
            conn.close()
    return False  # Ensure connection failure handling


def authenticate_user(username, password):
    conn = create_connection()
    if conn is not None:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT password FROM pengguna WHERE username = %s;"
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                if user and user['password'] == password:  # Replace with password check if using hashing
                    return True
                else:
                    return False
        except Exception as e:
            logger.error("Error in authenticate_user: %s", e)
            return False
        finally:
            conn.close()
    else:
        return False
