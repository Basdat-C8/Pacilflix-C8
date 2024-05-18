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