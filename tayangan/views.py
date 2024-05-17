from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from psycopg2.extras import RealDictCursor
from django.utils import timezone
import logging

from login_register.query import create_connection

logger = logging.getLogger(__name__)

def show_tayangan(request):
    conn = create_connection()
    if conn is not None:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Check if the user has an active package
                cursor.execute("""
                    SELECT * FROM TRANSACTION 
                    WHERE username = %s AND end_date_time > NOW()
                """, (request.session.get('username'),))
                has_active_package = cursor.fetchone() is not None

                # Fetch films
                cursor.execute("""
                    SELECT id_tayangan, judul, sinopsis_trailer, url_video_trailer, release_date_trailer
                    FROM FILM JOIN TAYANGAN ON FILM.id_tayangan = TAYANGAN.id;
                """)
                films = cursor.fetchall()

                # Fetch series
                cursor.execute("""
                    SELECT id_tayangan, judul, sinopsis_trailer, url_video_trailer, release_date_trailer
                    FROM SERIES JOIN TAYANGAN ON SERIES.id_tayangan = TAYANGAN.id;""")
                series = cursor.fetchall()

                context = {
                    'films': films,
                    'series': series,
                    'is_authenticated': bool(request.session.get('username')),
                    'use_navbar2': bool(request.session.get('username')),
                    'has_active_package': has_active_package,
                }
                return render(request, "tayangan_read.html", context)
        except Exception as e:
            logger.error("Error in fetching tayangan: %s", e)
            return render(request, "tayangan_read.html", {'use_navbar2': bool(request.session.get('username')), 'is_authenticated': bool(request.session.get('username'))})
        finally:
            conn.close()
    else:
        return render(request, "tayangan_read.html", {'use_navbar2': bool(request.session.get('username')), 'is_authenticated': bool(request.session.get('username'))})

def search_results(request):
    search_query = request.GET.get('search', '')
    conn = create_connection()
    if conn is not None:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Check if the user has an active package
                cursor.execute("SELECT * FROM TRANSACTION WHERE username = %s AND end_date_time > NOW()", (request.session.get('username'),))
                has_active_package = cursor.fetchone() is not None

                results = []

                if search_query:
                    # Fetch films
                    cursor.execute("""
                        SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer 
                        FROM TAYANGAN t
                        JOIN FILM f ON f.id_tayangan=t.id
                        WHERE judul ILIKE %s
                    """, ('%' + search_query + '%',))
                    films = cursor.fetchall()
                    for film in films:
                        film['type'] = 'FILM'
                    results.extend(films)

                    # Fetch series
                    cursor.execute("""
                        SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer 
                        FROM TAYANGAN t
                        JOIN SERIES s ON s.id_tayangan=t.id
                        WHERE judul ILIKE %s
                    """, ('%' + search_query + '%',))
                    series = cursor.fetchall()
                    for serie in series:
                        serie['type'] = 'SERIES'
                    results.extend(series)

                context = {
                    'results': results,
                    'use_navbar2': bool(request.session.get('username')),
                    'is_authenticated': bool(request.session.get('username')),
                    'has_active_package': has_active_package,
                }
                return render(request, 'search_results.html', context)
        except Exception as e:
            logger.error("Error in fetching search results: %s", e)
            return render(request, 'search_results.html', {'use_navbar2': bool(request.session.get('username')), 'is_authenticated': bool(request.session.get('username'))})
        finally:
            conn.close()
    else:
        return render(request, 'search_results.html', {'use_navbar2': bool(request.session.get('username')), 'is_authenticated': bool(request.session.get('username'))})

def show_film_details(request, id_tayangan):
    conn = create_connection()
    if conn is not None:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Fetch film and general details
                cursor.execute("""
                    SELECT t.*, f.url_video_film, f.release_date_film, f.durasi_film 
                    FROM FILM f
                    JOIN TAYANGAN t ON f.id_tayangan = t.id 
                    WHERE f.id_tayangan = %s;
                """, (id_tayangan,))
                film = cursor.fetchone()

                # Fetch genres
                cursor.execute("""
                    SELECT gt.genre 
                    FROM GENRE_TAYANGAN gt
                    JOIN FILM f ON f.id_tayangan = gt.id_tayangan
                    WHERE gt.id_tayangan = %s;
                """, (id_tayangan,))
                genres = [row['genre'] for row in cursor.fetchall()]

                # Fetch actors
                cursor.execute("""
                    SELECT c.nama
                    FROM PEMAIN p
                    JOIN MEMAINKAN_TAYANGAN mt ON p.id = mt.id_pemain
                    JOIN CONTRIBUTORS c ON c.id = mt.id_pemain
                    WHERE mt.id_tayangan = %s;
                """, (id_tayangan,))
                actors = [row['nama'] for row in cursor.fetchall()]

                # Fetch writers
                cursor.execute("""
                    SELECT c.nama 
                    FROM PENULIS_SKENARIO ps
                    JOIN MENULIS_SKENARIO_TAYANGAN mst ON ps.id = mst.id_penulis_skenario
                    JOIN CONTRIBUTORS c ON ps.id = c.id
                    WHERE mst.id_tayangan = %s;
                """, (id_tayangan,))
                writers = [row['nama'] for row in cursor.fetchall()]

                # Fetch sutradara
                cursor.execute("""
                    SELECT c.nama 
                    FROM SUTRADARA s
                    JOIN TAYANGAN t ON s.id = t.id_sutradara
                    JOIN CONTRIBUTORS c ON s.id = c.id
                    WHERE t.id = %s;
                """, (id_tayangan,))
                sutradara = cursor.fetchone()['nama']

                # Fetch reviews
                cursor.execute("""
                    SELECT u.username, u.rating, u.timestamp, u.deskripsi
                    FROM ULASAN u
                    WHERE u.id_tayangan = %s;
                """, (id_tayangan,))
                reviews = cursor.fetchall()

                context = {
                    'id_tayangan': id_tayangan,
                    'film': film,
                    'genres': genres,
                    'actors': actors,
                    'writers': writers,
                    'sutradara': sutradara,
                    'reviews': reviews,
                    'use_navbar2': bool(request.session.get('username')),
                    'is_authenticated': bool(request.session.get('username')),
                }
                return render(request, "film_details.html", context)
        except Exception as e:
            logger.error("Error in fetching film details: %s", e)
            return render(request, "film_details.html", {'use_navbar2': bool(request.session.get('username'))})
        finally:
            conn.close()
    else:
        return render(request, "film_details.html", {'use_navbar2': bool(request.session.get('username'))})

def submit_review_film(request, id_tayangan):
    if request.method == 'POST':
        review_text = request.POST.get('reviewText')
        rating = request.POST.get('rating')
        username = request.session.get('username')

        conn = create_connection()
        if conn is not None:
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Insert review
                    cursor.execute("""
                        INSERT INTO ULASAN (username, id_tayangan, deskripsi, rating, timestamp)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, (username, id_tayangan, review_text, rating))

                    conn.commit()

            except Exception as e:
                logger.error("Error in submitting review: %s", e)

            finally:
                conn.close()

        # Redirect back
        return HttpResponseRedirect(reverse('tayangan:show_film_details', args=(id_tayangan,)))

    else:
        return redirect('tayangan:show_film_details', id=id_tayangan)

def submit_review_series(request, id_tayangan):
    if request.method == 'POST':
        review_text = request.POST.get('reviewText')
        rating = request.POST.get('rating')
        username = request.session.get('username')

        conn = create_connection()
        if conn is not None:
            try:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    # Insert review
                    cursor.execute("""
                        INSERT INTO ULASAN (username, id_tayangan, deskripsi, rating, timestamp)
                        VALUES (%s, %s, %s, %s, NOW())
                    """, (username, id_tayangan, review_text, rating))

                    conn.commit()

            except Exception as e:
                logger.error("Error in submitting review: %s", e)

            finally:
                conn.close()

        # Redirect back
        return HttpResponseRedirect(reverse('tayangan:show_series_details', args=(id_tayangan,)))

    else:
        return redirect('tayangan:show_series_details', id=id_tayangan)

def show_series_details(request, id_tayangan):
    conn = create_connection()
    if conn is not None:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Fetch series and general details
                cursor.execute("""
                    SELECT t.*, se.*
                    FROM SERIES se
                    JOIN TAYANGAN t ON se.id_tayangan = t.id 
                    WHERE se.id_tayangan = %s;
                """, (id_tayangan,))
                series = cursor.fetchone()

                # Fetch genres
                cursor.execute("""
                    SELECT gt.genre 
                    FROM GENRE_TAYANGAN gt
                    JOIN SERIES se ON se.id_tayangan = gt.id_tayangan
                    WHERE gt.id_tayangan = %s;
                """, (id_tayangan,))
                genres = [row['genre'] for row in cursor.fetchall()]

                # Fetch actors
                cursor.execute("""
                    SELECT c.nama
                    FROM PEMAIN p
                    JOIN MEMAINKAN_TAYANGAN mt ON p.id = mt.id_pemain
                    JOIN CONTRIBUTORS c ON c.id = mt.id_pemain
                    WHERE mt.id_tayangan = %s;
                """, (id_tayangan,))
                actors = [row['nama'] for row in cursor.fetchall()]

                # Fetch writers
                cursor.execute("""
                    SELECT c.nama 
                    FROM PENULIS_SKENARIO ps
                    JOIN MENULIS_SKENARIO_TAYANGAN mst ON ps.id = mst.id_penulis_skenario
                    JOIN CONTRIBUTORS c ON ps.id = c.id
                    WHERE mst.id_tayangan = %s;
                """, (id_tayangan,))
                writers = [row['nama'] for row in cursor.fetchall()]

                # Fetch sutradara
                cursor.execute("""
                    SELECT c.nama 
                    FROM SUTRADARA s
                    JOIN TAYANGAN t ON s.id = t.id_sutradara
                    JOIN CONTRIBUTORS c ON s.id = c.id
                    WHERE t.id = %s;
                """, (id_tayangan,))
                sutradara = cursor.fetchone()['nama']

                # Fetch reviews
                cursor.execute("""
                    SELECT u.username, u.rating, u.timestamp, u.deskripsi
                    FROM ULASAN u
                    WHERE u.id_tayangan = %s;
                """, (id_tayangan,))
                reviews = cursor.fetchall()

                # Fetch episodes
                cursor.execute("""
                    SELECT e.*, row_number() OVER (ORDER BY e.release_date ASC) as listing_order
                    FROM EPISODE e
                    WHERE e.id_series = %s;
                """, (id_tayangan,))
                episodes = cursor.fetchall()

                context = {
                    'id_tayangan': id_tayangan,
                    'series': series,
                    'genres': genres,
                    'actors': actors,
                    'writers': writers,
                    'sutradara': sutradara,
                    'reviews': reviews,
                    'episodes': episodes,
                    'use_navbar2': bool(request.session.get('username')),
                    'is_authenticated': bool(request.session.get('username')),
                }
                return render(request, "series_details.html", context)
        except Exception as e:
            logger.error("Error in fetching series details: %s", e)
            return render(request, "series_details.html", {'use_navbar2': bool(request.session.get('username'))})
        finally:
            conn.close()
    else:
        return render(request, "series_details.html", {'use_navbar2': bool(request.session.get('username'))})

def show_episode_details(request, id_series, sub_judul):
    conn = create_connection()
    if conn is not None:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Fetch all episodes for the series

                cursor.execute("SELECT judul FROM TAYANGAN WHERE id = %s", (id_series,))
                series_name = cursor.fetchone()['judul']

                cursor.execute("""
                    SELECT e.*, row_number() OVER (ORDER BY e.release_date ASC) as listing_order
                    FROM EPISODE e
                    WHERE e.id_series = %s
                    ORDER BY e.release_date ASC;
                """, (id_series,))
                episodes = cursor.fetchall()

                # Filter the correct episode
                episode = next((ep for ep in episodes if ep['sub_judul'] == sub_judul), None)

                # Remove the current episode from the episodes list
                episodes = [ep for ep in episodes if ep['sub_judul'] != sub_judul]

                context = {
                    'series_name': series_name,
                    'episodes': episodes,
                    'episode': episode,
                    'use_navbar2': bool(request.session.get('username')),
                    'is_authenticated': bool(request.session.get('username')),
                }
                return render(request, "episode_details.html", context)
        except Exception as e:
            logger.error("Error in fetching episode details: %s", e)
            return render(request, "episode_details.html", {'use_navbar2': bool(request.session.get('username'))})
        finally:
            conn.close()
    else:
        return render(request, "episode_details.html", {'use_navbar2': bool(request.session.get('username'))})

def watch_episode(request, id_series):
    connection = create_connection()
    if request.method == 'POST':
        progress = request.POST.get('progress')
        username = request.session.get('username')
        # Save the watching activity to the RIWAYAT_NONTON table
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO RIWAYAT_NONTON (username, id_tayangan, progress, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (username, id_series, progress, timezone.now()))
        return redirect('episode_details', id_series=id_series)


def show_daftar_kontributor(request):
    context = {'use_navbar2': True}
    return render(request, "daftar_kontributor_read.html", context)