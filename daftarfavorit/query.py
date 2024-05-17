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

def query_get_all_users_daftar_favorit(username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(f"select * from daftar_favorit where username='{username}';")
    return cursor.fetchall()

def query_get_specific_daftar_favorit(timestamp, username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(f"select * from daftar_favorit where username='{username}' AND timestamp='{timestamp}';")
    return cursor.fetchone()

def query_get_tayangan_daftar_favorit(timestamp, username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(rf""" 
        select b.judul, a.id_tayangan, a.timestamp, a.username
        from (select * from tayangan_memiliki_daftar_favorit where timestamp='{timestamp}' AND username='{username}') AS a JOIN
        (select judul, id from tayangan) AS b ON b.id=a.id_tayangan;
    """)
    return cursor.fetchall()


# ========================================= delete

def query_delete_daftar_favorit(timestamp, username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(f"delete from daftar_favorit where username='{username}' AND timestamp='{timestamp}';")
    connection.commit()

def query_delete_tayangan(id_tayangan, timestamp, username):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(f"delete from tayangan_memiliki_daftar_favorit where id_tayangan='{id_tayangan}' AND username='{username}' AND timestamp='{timestamp}';")
    connection.commit()

