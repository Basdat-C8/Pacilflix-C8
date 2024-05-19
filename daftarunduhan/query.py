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
    

# ========================================= get

def query_get_downloaded_tayangan(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(rf"""
                   select b.judul, a.id_tayangan, a.username, a.timestamp
        from (select * from tayangan_terunduh where username='{username}') AS a JOIN
        (select judul, id from tayangan) AS b ON b.id=a.id_tayangan;
                   """)
    return cursor.fetchall()

# ========================================= delete

def query_delete_unduhan(id_tayangan, timestamp, username):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(f"delete from tayangan_terunduh where id_tayangan='{id_tayangan}' AND username='{username}' AND timestamp='{timestamp}';")
        connection.commit()
        return "success"

    except psycopg2.Error as err:
        return str(err)