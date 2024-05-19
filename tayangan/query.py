top_10_global = """
    SELECT 
        ROW_NUMBER() OVER (ORDER BY COALESCE(SUM(valid_watch_sessions.watch_valid), 0) DESC, t.judul ASC) AS Rank,
        t.id,
        t.judul AS Judul,
        t.sinopsis AS Sinopsis_Trailer,
        t.url_video_trailer AS Trailer_URL,
        t.release_date_trailer AS Tanggal_Rilis_Trailer,
        COALESCE(SUM(valid_watch_sessions.watch_valid), 0) AS Total_View_7_Hari_Terakhir,
        CASE
            WHEN f.id_tayangan IS NOT NULL THEN 'FILM'
            WHEN s.id_tayangan IS NOT NULL THEN 'SERIES'
        END AS Type
    FROM TAYANGAN t
    LEFT JOIN FILM f ON f.id_tayangan = t.id
    LEFT JOIN SERIES s ON s.id_tayangan = t.id
    LEFT JOIN (
        -- Gabungan subquery untuk distinct series views and film views
        SELECT 
            id_tayangan,
            COUNT(*) AS watch_valid
        FROM (
            SELECT DISTINCT
                rn.id_tayangan,
                rn.username,
                rn.start_date_time,
                rn.end_date_time
            FROM RIWAYAT_NONTON rn
            JOIN EPISODE e ON e.id_series = rn.id_tayangan
            WHERE 
                (EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60) >= (e.durasi * 0.7)
                AND rn.end_date_time >= NOW() - INTERVAL '7 days'
            UNION ALL
            SELECT 
                rn.id_tayangan,
                rn.username,
                rn.start_date_time,
                rn.end_date_time
            FROM RIWAYAT_NONTON rn
            JOIN FILM f ON f.id_tayangan = rn.id_tayangan
            WHERE 
                (EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60) >= (f.durasi_film * 0.7)
                AND rn.end_date_time >= NOW() - INTERVAL '7 days'
        ) AS combined_views
        GROUP BY combined_views.id_tayangan
    ) valid_watch_sessions ON valid_watch_sessions.id_tayangan = t.id
    GROUP BY t.id, t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, f.id_tayangan, s.id_tayangan
    ORDER BY Total_View_7_Hari_Terakhir DESC, t.judul ASC
    LIMIT 10;
"""

top_10_local = """
SELECT 
	ROW_NUMBER() OVER (ORDER BY COALESCE(SUM(valid_watch_sessions.watch_valid), 0) DESC, t.judul ASC) AS Rank,
	t.id,
	t.judul AS Judul,
	t.sinopsis AS Sinopsis_Trailer,
	t.url_video_trailer AS Trailer_URL,
	t.release_date_trailer AS Tanggal_Rilis_Trailer,
	COALESCE(SUM(valid_watch_sessions.watch_valid), 0) AS Total_View_7_Hari_Terakhir,
	CASE
		WHEN f.id_tayangan IS NOT NULL THEN 'FILM'
		WHEN s.id_tayangan IS NOT NULL THEN 'SERIES'
	END AS Type
FROM TAYANGAN t
LEFT JOIN FILM f ON f.id_tayangan = t.id
LEFT JOIN SERIES s ON s.id_tayangan = t.id
LEFT JOIN (
	-- Gabungan subquery untuk distinct series views and film views
	SELECT 
		id_tayangan,
		COUNT(*) AS watch_valid
	FROM (
		SELECT DISTINCT
			rn.id_tayangan,
			rn.username,
			rn.start_date_time,
			rn.end_date_time
		FROM RIWAYAT_NONTON rn
		JOIN EPISODE e ON e.id_series = rn.id_tayangan
		WHERE 
			(EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60) >= (e.durasi * 0.7)
			AND rn.end_date_time >= NOW() - INTERVAL '7 days'
		UNION ALL
		SELECT 
			rn.id_tayangan,
			rn.username,
			rn.start_date_time,
			rn.end_date_time
		FROM RIWAYAT_NONTON rn
		JOIN FILM f ON f.id_tayangan = rn.id_tayangan
		WHERE 
			(EXTRACT(EPOCH FROM (rn.end_date_time - rn.start_date_time)) / 60) >= (f.durasi_film * 0.7)
			AND rn.end_date_time >= NOW() - INTERVAL '7 days'
	) AS combined_views
	GROUP BY combined_views.id_tayangan
) valid_watch_sessions ON valid_watch_sessions.id_tayangan = t.id
JOIN PENGGUNA p ON p.negara_asal = t.asal_negara
GROUP BY t.id, t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, f.id_tayangan, s.id_tayangan
ORDER BY Total_View_7_Hari_Terakhir DESC, t.judul ASC
LIMIT 10;
"""

# ========================================================================================

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

# ========================================= add

def query_add_to_daftar_favorit(username, timestamp, id_tayangan):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(f"INSERT INTO TAYANGAN_MEMILIKI_DAFTAR_FAVORIT VALUES ('{id_tayangan}','{timestamp}','{username}');")
    connection.commit()

def query_add_to_daftar_unduhan(username, id_tayangan):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute(rf"""
                   set timezone to 'Asia/Jakarta';
                   INSERT INTO TAYANGAN_TERUNDUH VALUES ('{id_tayangan}','{username}', date_trunc('second', CURRENT_TIMESTAMP));
                   """)
    connection.commit()