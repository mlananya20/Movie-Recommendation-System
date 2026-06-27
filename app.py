

# import streamlit as st
# import requests
# import pandas as pd
# import re
# import time
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# from recommender import recommend
# from concurrent.futures import ThreadPoolExecutor
# import random

# st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
# st.markdown("""
#     <style>
#     [data-testid="stStatusWidget"] { display: none; }
#     </style>
# """, unsafe_allow_html=True)
# TMDB_API_KEY = "c693c69d66e8db29bb9bcde74c2f2f55"

# GENRE_MAP = {
#     28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
#     80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
#     14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
#     9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV Movie",
#     53: "Thriller", 10752: "War", 37: "Western"
# }

# def get_session():
#     session = requests.Session()
#     retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount("https://", adapter)
#     return session

# @st.cache_data
# def fetch_movie_details(title, api_key):
#     time.sleep(random.uniform(0.1, 0.4))
#     clean_title = re.sub(r'\(\d{4}\)', '', title).strip()
#     clean_title = re.sub(r'^(.*),\s*(The|A|An)$', r'\2 \1', clean_title, flags=re.IGNORECASE).strip()
#     clean_title = clean_title.strip(',').strip()
#     print(f"Searching TMDB for: '{clean_title}'")

#     try:
#         session = get_session()
#         year_match = re.search(r'\((\d{4})\)', title)
#         url = "https://api.themoviedb.org/3/search/movie"
#         params = {"api_key": api_key, "query": clean_title}

#         res = session.get(url, params=params, timeout=15).json()
#         results = res.get("results", [])

#         if results and year_match:
#             year_hint = year_match.group(1)
#             for r in results:
#                 if r.get("release_date", "").startswith(year_hint):
#                     results[0] = r
#                     break

#         # if not results:
#         #     return None, "N/A", "N/A", "N/A"
#         # After your existing results check, before "if not results:"
#         if not results or not results[0].get("poster_path"):
#             # Fallback: try just first 2 words
#             short_title = " ".join(clean_title.split()[:2])
#             res2 = session.get(url, params={"api_key": api_key, "query": short_title}, timeout=15).json()
#             results2 = res2.get("results", [])
#             if results2 and year_match:
#                 year_hint = year_match.group(1)
#                 for r in results2:
#                     if r.get("release_date", "").startswith(year_hint):
#                         results = [r]
#                         break
#             elif results2:
#                 results = results2

#         m = results[0]
#         poster = f"https://image.tmdb.org/t/p/w300{m['poster_path']}" if m.get("poster_path") else None
#         year = m.get("release_date", "N/A")[:4]
#         rating = round(m.get("vote_average", 0), 1)
#         genre_ids = m.get("genre_ids", [])
#         genres = ", ".join([GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP])
#         return poster, year, genres, rating

#     except Exception as e:
#         return None, "N/A", "N/A", "N/A"

# # Load titles
# movies_df = pd.read_csv("data/movies.csv")
# titles = [""] + movies_df["title"].dropna().tolist()

# st.title("🎬 Movie Recommendation System")
# st.write("Search a movie you like and get 5 similar movies with posters!")

# query = st.selectbox("🔍 Search a movie:", options=titles)

# if st.button("Get Recommendations"):
#     if not query:
#         st.warning("Please select a movie.")
#     else:
#         results = recommend(query)
#         if isinstance(results[0], str) and "not found" in results[0].lower():
#             st.error(results[0])
#         else:
#             with st.spinner("Fetching recommendations..."):
#                 # with ThreadPoolExecutor(max_workers=5) as executor:
#                 #     movie_details = list(executor.map(lambda m: fetch_movie_details(m, TMDB_API_KEY), results))
#                 movie_details = []
#                 for m in results:
#                     details = fetch_movie_details(m, TMDB_API_KEY)
#                     movie_details.append(details)
#                     time.sleep(0.25)

#             st.subheader("You might also like:")
#             cols = st.columns(5)

#             # Fetch all 5 movies in parallel
#             with ThreadPoolExecutor(max_workers=5) as executor:
#                 movie_details = list(executor.map(lambda m: fetch_movie_details(m, TMDB_API_KEY), results))

#             for col, movie, details in zip(cols, results, movie_details):
#                 with col:
#                     poster, year, genres, rating = details
#                     if poster:
#                         st.image(poster, width='stretch')
#                     else:
#                         st.image("https://placehold.co/200x300?text=No+Poster", width='stretch')
#                     st.markdown(f"**{movie}**")
#                     st.caption(f"⭐ {rating}/10  |  📅 {year}")
#                     st.caption(f"🎭 {genres}")


# import streamlit as st
# import requests
# import pandas as pd
# import re
# import time
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# from recommender import recommend
# # from concurrent.futures import ThreadPoolExecutor
# import random

# st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
# st.markdown("""
#     <style>
#     [data-testid="stStatusWidget"] { display: none; }
#     </style>
# """, unsafe_allow_html=True)

# TMDB_API_KEY = "c693c69d66e8db29bb9bcde74c2f2f55"

# GENRE_MAP = {
#     28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
#     80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
#     14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
#     9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV Movie",
#     53: "Thriller", 10752: "War", 37: "Western"
# }

# def get_session():
#     session = requests.Session()
#     retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount("https://", adapter)
#     return session

# # @st.cache_data
# # #def fetch_movie_details(title, api_key):
# # def fetch_movie_details(movie_id, api_key):
# #     """Fetch movie details from TMDB API with fallback strategies"""
# #     time.sleep(random.uniform(0.1, 0.4))
# #     # clean_title = re.sub(r'\(\d{4}\)', '', title).strip()
# #     # clean_title = re.sub(r'^(.*),\s*(The|A|An)$', r'\2 \1', clean_title, flags=re.IGNORECASE).strip()
# #     # clean_title = clean_title.strip(',').strip()
    
# #     # print(f"🔍 Searching TMDB for: '{clean_title}' (Original: '{title}')")

# #     try:
# #         session = get_session()
# #         # year_match = re.search(r'\((\d{4})\)', title)
# #         # url = "https://api.themoviedb.org/3/search/movie"
        
# #         # # First attempt: full cleaned title
# #         # params = {"api_key": api_key, "query": clean_title}
# #         # res = session.get(url, params=params, timeout=15).json()
# #         # results = res.get("results", [])
# #         url = f"https://api.themoviedb.org/3/movie/{movie_id}"

# #         params = {
# #             "api_key": api_key
# #         }

# #         m = session.get(url, params=params, timeout=15).json()

        
   
# #         # poster = f"https://image.tmdb.org/t/p/w300{m['poster_path']}" if m.get("poster_path") else None
# #         # year = m.get("release_date", "N/A")[:4]
# #         # rating = round(m.get("vote_average", 0), 1)
# #         # # genre_ids = m.get("genre_ids", [])
# #         # genre_ids = [g["id"] for g in m.get("genres", [])]
# #         # genres = ", ".join([GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP])
        
# #         # print(f"  ✅ Found: {m.get('title')} ({year}) - Poster: {'Yes' if poster else 'No'}")
# #         # return poster, year, genres, rating

# #         poster = (
# #             f"https://image.tmdb.org/t/p/w300{m['poster_path']}"
# #             if m.get("poster_path")
# #             else None
# #         )

# #         year = m.get("release_date", "N/A")[:4]
# #         rating = round(m.get("vote_average", 0), 1)

# #         genre_ids = [g["id"] for g in m.get("genres", [])]
# #         genres = ", ".join(
# #             [GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP]
# #         )

# #         return poster, year, genres, rating

# #     # except Exception as e:
# #     #     print(f"  ❌ Error fetching '{title}': {str(e)}")
# #     #     return None, "N/A", "N/A", "N/A"
# #     except Exception as e:
# #         print(f"❌ Error: {str(e)}")
# #         return None, "N/A", "N/A", "N/A"






# # @st.cache_data
# # def fetch_movie_details(movie_id, api_key, title=""):
# #     time.sleep(random.uniform(0.1, 0.4))
# #     try:
# #         session = get_session()

# #         # ── Step 1: Try by movie_id ──────────────────────────────
# #         url = f"https://api.themoviedb.org/3/movie/{movie_id}"
# #         m = session.get(url, params={"api_key": api_key}, timeout=15).json()

# #         got_poster  = bool(m.get("poster_path"))
# #         got_details = bool(m.get("release_date") and m.get("vote_average"))

# #         # ── Step 2: Fallback by title search if anything is missing ─
# #         if (not got_poster or not got_details) and title:
# #             search_url = "https://api.themoviedb.org/3/search/movie"
# #             res = session.get(
# #                 search_url,
# #                 params={"api_key": api_key, "query": title},
# #                 timeout=15
# #             ).json()
# #             results = res.get("results", [])

# #             if results:
# #                 # Pick best match — prefer exact title match
# #                 best = None
# #                 for r in results:
# #                     if r.get("title", "").lower() == title.lower():
# #                         best = r
# #                         break
# #                 if not best:
# #                     best = results[0]  # fallback to first result

# #                 # Only override fields that were missing
# #                 if not got_poster and best.get("poster_path"):
# #                     m["poster_path"] = best["poster_path"]
# #                 if not got_details:
# #                     m["release_date"]  = best.get("release_date", "")
# #                     m["vote_average"]  = best.get("vote_average", 0)
# #                     m["genre_ids"]     = best.get("genre_ids", [])

# #         # ── Step 3: Build final result ───────────────────────────
# #         poster = (
# #             f"https://image.tmdb.org/t/p/w300{m['poster_path']}"
# #             if m.get("poster_path") else None
# #         )
# #         year   = m.get("release_date", "N/A")[:4] or "N/A"
# #         rating = round(float(m.get("vote_average") or 0), 1)

# #         # genres: movie detail endpoint returns list of dicts; search returns id list
# #         if "genres" in m and isinstance(m["genres"], list) and m["genres"] and isinstance(m["genres"][0], dict):
# #             genre_ids = [g["id"] for g in m["genres"]]
# #         else:
# #             genre_ids = m.get("genre_ids", [])

# #         genres = ", ".join([GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP])

# #         return poster, year, genres, rating

# #     except Exception as e:
# #         print(f"❌ Error for movie_id={movie_id}, title='{title}': {str(e)}")
# #         return None, "N/A", "N/A", "N/A"
# @st.cache_data
# def fetch_movie_details(movie_id, api_key, title=""):
#     time.sleep(random.uniform(0.1, 0.4))
#     try:
#         session = get_session()
#         m = {}
        
#         # Step 1: Try by movie_id
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}"
#         resp = session.get(url, params={"api_key": api_key}, timeout=15)
#         if resp.status_code == 200:
#             m = resp.json()
#             print(f"   poster={m.get('poster_path')}, year={m.get('release_date')}")
#         # Step 2: Always try title search if poster is missing
#         if not m.get("poster_path") and title:
#             clean_title = re.sub(r'\(\d{4}\)', '', title).strip()
#             search_url = "https://api.themoviedb.org/3/search/movie"
#             res = session.get(
#                 search_url,
#                 params={"api_key": api_key, "query": clean_title},
#                 timeout=15
#             ).json()
#             results = res.get("results", [])
#             print(f"🔎 Search results count={len(results)}")
#             if results:
#                 # prefer exact match, else first result
#                 best = next((r for r in results if r.get("title","").lower() == clean_title.lower()), results[0])
#                 # merge missing fields
#                 for field in ["poster_path", "release_date", "vote_average", "genre_ids"]:
#                     if not m.get(field):
#                         m[field] = best.get(field)

#         # Step 3: Build result
#         poster = f"https://image.tmdb.org/t/p/w300{m['poster_path']}" if m.get("poster_path") else None
#         year   = (m.get("release_date") or "N/A")[:4] or "N/A"
#         rating = round(float(m.get("vote_average") or 0), 1)

#         if "genres" in m and isinstance(m.get("genres"), list) and m["genres"] and isinstance(m["genres"][0], dict):
#             genre_ids = [g["id"] for g in m["genres"]]
#         else:
#             genre_ids = m.get("genre_ids", [])

#         genres = ", ".join([GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP])
#         return poster, year, genres, rating

#     except Exception as e:
#         print(f"❌ Error for movie_id={movie_id}, title='{title}': {str(e)}")
#         return None, "N/A", "N/A", "N/A"
    
# # Load titles
# #movies_df = pd.read_csv("data/movies.csv")
# movies_df = pd.read_csv("data/tmdb_5000_movies.csv")

# titles = [""] + movies_df["title"].dropna().tolist()

# st.title("🎬 Movie Recommendation System")
# st.write("Search a movie you like and get 5 similar movies with posters!")

# query = st.selectbox("🔍 Search a movie:", options=titles)

# if st.button("Get Recommendations"):
#     if not query:
#         st.warning("Please select a movie.")
#     else:
#         results = recommend(query)
#         if isinstance(results, list) and isinstance(results[0], str) and "not found" in results[0].lower():
#             st.error(results[0])
#         else:
#             with st.spinner("Fetching recommendations..."):
#                  movie_details = []
#                  for r in results:
#                      time.sleep(random.uniform(0.8, 1.2))
#                      movie_details.append(fetch_movie_details(r["movie_id"], TMDB_API_KEY, title=r["title"]))
            
#                 # def fetch_with_delay(r):
#                 #     time.sleep(random.uniform(0.3, 0.8))
#                 #     return fetch_movie_details(r["movie_id"], TMDB_API_KEY, title=r["title"])
#                 # def fetch_with_delay(r):
#                 #     for attempt in range(3):  # retry up to 3 times
#                 #         try:
#                 #          time.sleep(random.uniform(0.3, 0.8))
#                 #          result = fetch_movie_details(r["movie_id"], TMDB_API_KEY, title=r["title"])
#                 #          if result[0] is not None:  # got a poster
#                 #              return result
#                 #         except Exception:
#                 #             time.sleep(1.5 * (attempt + 1))
#                 #     return fetch_movie_details(r["movie_id"], TMDB_API_KEY, title=r["title"])
#                 # def fetch_with_delay(r):
#                 #     for attempt in range(3):
#                 #         try:
#                 #            time.sleep(random.uniform(0.5 * (attempt + 1), 1.0 * (attempt + 1)))
#                 #            result = fetch_movie_details.clear()  # won't help in thread, skip
#                 #            result = fetch_movie_details.__wrapped__(r["movie_id"], TMDB_API_KEY, title=r["title"])
#                 #            return result
#                 #         except Exception:
#                 #            pass
#                 #     return None, "N/A", "N/A", "N/A"

#                 #  with ThreadPoolExecutor(max_workers=3) as executor:
#                 #     movie_details = list(executor.map(fetch_with_delay, results))

#             st.subheader("You might also like:")
#             cols = st.columns(5)

#             for col, movie, details in zip(cols, results, movie_details):
#                 with col:
#                     poster, year, genres, rating = details
#                     if poster:
#                         st.image(poster, width='stretch')
#                     else:
#                         st.image("https://placehold.co/200x300?text=No+Poster", width='stretch')
#                         # st.warning("Poster not available")
#                     st.markdown(f"**{movie['title']}**")
#                     st.caption(f"⭐ {rating}/10  |  📅 {year}")
#                     st.caption(f"🎭 {genres}")
#                     st.caption(f"🎬 {movie['director']}")
#                     st.caption(f"👥 {movie['cast']}")
#                     st.caption(f"🏷️ {movie['keywords']}")
#                     # ── V4 additions ──
#                     mode_icon = "🔀" if movie.get("mode") == "hybrid" else "📐"
#                     st.caption(f"{mode_icon} Match score: {movie.get('score', 'N/A')}")

# import streamlit as st
# import requests
# import pandas as pd
# import re
# import time
# import random
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
# from recommender import recommend
# from sentiment import fetch_sentiment   # ── V6 ──

# st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
# st.markdown("""
#     <style>
#     [data-testid="stStatusWidget"] { display: none; }

#     /* ── V6: sentiment bar styles ── */
#     .sent-bar-wrap { width:100%; background:#e0e0e0; border-radius:6px; height:8px; margin:2px 0 4px 0; }
#     .sent-bar-pos  { background:#4caf50; height:8px; border-radius:6px; }
#     .sent-bar-neg  { background:#f44336; height:8px; border-radius:6px; }
#     .sent-bar-neu  { background:#9e9e9e; height:8px; border-radius:6px; }
#     .sent-label    { font-size:0.72rem; color:#555; margin-bottom:2px; }
#     </style>
# """, unsafe_allow_html=True)

# TMDB_API_KEY = "c693c69d66e8db29bb9bcde74c2f2f55"

# GENRE_MAP = {
#     28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
#     80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
#     14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
#     9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV Movie",
#     53: "Thriller", 10752: "War", 37: "Western"
# }


# def get_session():
#     session = requests.Session()
#     retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount("https://", adapter)
#     return session


# @st.cache_data
# def fetch_movie_details(movie_id, api_key, title=""):
#     time.sleep(random.uniform(0.1, 0.4))
#     try:
#         session = get_session()
#         m = {}

#         url = f"https://api.themoviedb.org/3/movie/{movie_id}"
#         resp = session.get(url, params={"api_key": api_key}, timeout=15)
#         if resp.status_code == 200:
#             m = resp.json()
#             print(f"   poster={m.get('poster_path')}, year={m.get('release_date')}")

#         if not m.get("poster_path") and title:
#             clean_title = re.sub(r'\(\d{4}\)', '', title).strip()
#             search_url = "https://api.themoviedb.org/3/search/movie"
#             res = session.get(
#                 search_url,
#                 params={"api_key": api_key, "query": clean_title},
#                 timeout=15
#             ).json()
#             results = res.get("results", [])
#             print(f"🔎 Search results count={len(results)}")
#             if results:
#                 best = next(
#                     (r for r in results if r.get("title", "").lower() == clean_title.lower()),
#                     results[0]
#                 )
#                 for field in ["poster_path", "release_date", "vote_average", "genre_ids"]:
#                     if not m.get(field):
#                         m[field] = best.get(field)

#         poster = f"https://image.tmdb.org/t/p/w300{m['poster_path']}" if m.get("poster_path") else None
#         year   = (m.get("release_date") or "N/A")[:4] or "N/A"
#         rating = round(float(m.get("vote_average") or 0), 1)

#         if "genres" in m and isinstance(m.get("genres"), list) and m["genres"] and isinstance(m["genres"][0], dict):
#             genre_ids = [g["id"] for g in m["genres"]]
#         else:
#             genre_ids = m.get("genre_ids", [])

#         genres = ", ".join([GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP])
#         return poster, year, genres, rating

#     except Exception as e:
#         print(f"❌ Error for movie_id={movie_id}, title='{title}': {str(e)}")
#         return None, "N/A", "N/A", "N/A"


# # ── V6: cached sentiment fetch ───────────────────────────────────
# @st.cache_data
# def fetch_sentiment_cached(movie_id, api_key):
#     return fetch_sentiment(movie_id, api_key)


# def render_sentiment_bar(label, pct, color_class):
#     """Render a single labelled progress bar via HTML."""
#     st.markdown(
#         f'<div class="sent-label">{label} {pct}%</div>'
#         f'<div class="sent-bar-wrap"><div class="{color_class}" style="width:{pct}%"></div></div>',
#         unsafe_allow_html=True
#     )


# # ── Load titles ──────────────────────────────────────────────────
# movies_df = pd.read_csv("data/tmdb_5000_movies.csv")
# titles = [""] + movies_df["title"].dropna().tolist()

# # ── UI ───────────────────────────────────────────────────────────
# st.title("🎬 Movie Recommendation System")
# st.write("Search a movie you like and get 5 similar movies with posters!")

# query = st.selectbox("🔍 Search a movie:", options=titles)

# # ── V6: toggle for sentiment panel ──────────────────────────────
# show_sentiment = st.toggle("🧠 Show Sentiment Analysis (NLP)", value=True)

# if st.button("Get Recommendations"):
#     if not query:
#         st.warning("Please select a movie.")
#     else:
#         # results = recommend(query)
#         results = recommend(query, movies_df, new_df, content_sim, collab_sim)
#         if isinstance(results, list) and isinstance(results[0], str) and "not found" in results[0].lower():
#             st.error(results[0])
#         else:
#             with st.spinner("Fetching recommendations..."):
#                 movie_details = []
#                 for r in results:
#                     time.sleep(random.uniform(0.8, 1.2))
#                     movie_details.append(fetch_movie_details(r["movie_id"], TMDB_API_KEY, title=r["title"]))

#             # ── V6: fetch sentiment sequentially ────────────────
#             sentiment_data = []
#             if show_sentiment:
#                 with st.spinner("Analysing reviews... 🧠"):
#                     for r in results:
#                         time.sleep(random.uniform(0.3, 0.6))
#                         sentiment_data.append(fetch_sentiment_cached(r["movie_id"], TMDB_API_KEY))
#             else:
#                 sentiment_data = [None] * len(results)

#             st.subheader("You might also like:")
#             cols = st.columns(5)

#             for col, movie, details, sent in zip(cols, results, movie_details, sentiment_data):
#                 with col:
#                     poster, year, genres, rating = details
#                     if poster:
#                         st.image(poster, width='stretch')
#                     else:
#                         st.image("https://placehold.co/200x300?text=No+Poster", width='stretch')

#                     st.markdown(f"**{movie['title']}**")
#                     st.caption(f"⭐ {rating}/10  |  📅 {year}")
#                     st.caption(f"🎭 {genres}")
#                     st.caption(f"🎬 {movie['director']}")
#                     st.caption(f"👥 {movie['cast']}")
#                     st.caption(f"🏷️ {movie['keywords']}")

#                     mode_icon = "🔀" if movie.get("mode") == "hybrid" else "📐"
#                     st.caption(f"{mode_icon} Match score: {movie.get('score', 'N/A')}")

#                     # ── V6: sentiment block ──────────────────────
#                     if show_sentiment and sent:
#                         st.markdown("---")
#                         if sent["total"] == 0:
#                             st.caption("💬 No reviews found")
#                         else:
#                             st.caption(f"💬 Reviews: {sent['total']}  |  {sent['label']}")
#                             render_sentiment_bar("✅ Positive", sent["pct_pos"], "sent-bar-pos")
#                             render_sentiment_bar("❌ Negative", sent["pct_neg"], "sent-bar-neg")
#                             render_sentiment_bar("➖ Neutral",  sent["pct_neu"], "sent-bar-neu")

#                             # Expandable review snippets
#                             if sent["reviews"]:
#                                 with st.expander("📝 Sample Reviews"):
#                                     for rev in sent["reviews"][:3]:
#                                         icon = {"positive": "✅", "negative": "❌", "neutral": "➖"}.get(rev["sentiment"], "")
#                                         st.markdown(f"{icon} **{rev['author']}**")
#                                         st.caption(rev["content"])
#                                         st.markdown("---")

import streamlit as st
import requests
import pandas as pd
import re
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from recommender import load_model, recommend
from sentiment import fetch_sentiment

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.markdown("""
    <style>
    [data-testid="stStatusWidget"] { display: none; }
    .sent-bar-wrap { width:100%; background:#e0e0e0; border-radius:6px; height:8px; margin:2px 0 4px 0; }
    .sent-bar-pos  { background:#4caf50; height:8px; border-radius:6px; }
    .sent-bar-neg  { background:#f44336; height:8px; border-radius:6px; }
    .sent-bar-neu  { background:#9e9e9e; height:8px; border-radius:6px; }
    .sent-label    { font-size:0.72rem; color:#555; margin-bottom:2px; }
    </style>
""", unsafe_allow_html=True)

TMDB_API_KEY = "c693c69d66e8db29bb9bcde74c2f2f55"

GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV Movie",
    53: "Thriller", 10752: "War", 37: "Western"
}


# ── Load model ONCE, cache forever in this session ──────────────
@st.cache_resource(show_spinner=False)
def get_model():
    return load_model()


def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


@st.cache_data
def fetch_movie_details(movie_id, api_key, title=""):
    time.sleep(random.uniform(0.1, 0.4))
    try:
        session = get_session()
        m = {}

        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        resp = session.get(url, params={"api_key": api_key}, timeout=15)
        if resp.status_code == 200:
            m = resp.json()

        if not m.get("poster_path") and title:
            clean_title = re.sub(r'\(\d{4}\)', '', title).strip()
            search_url = "https://api.themoviedb.org/3/search/movie"
            res = session.get(
                search_url,
                params={"api_key": api_key, "query": clean_title},
                timeout=15
            ).json()
            results = res.get("results", [])
            if results:
                best = next(
                    (r for r in results if r.get("title", "").lower() == clean_title.lower()),
                    results[0]
                )
                for field in ["poster_path", "release_date", "vote_average", "genre_ids"]:
                    if not m.get(field):
                        m[field] = best.get(field)

        poster = f"https://image.tmdb.org/t/p/w300{m['poster_path']}" if m.get("poster_path") else None
        year   = (m.get("release_date") or "N/A")[:4] or "N/A"
        rating = round(float(m.get("vote_average") or 0), 1)

        if "genres" in m and isinstance(m.get("genres"), list) and m["genres"] and isinstance(m["genres"][0], dict):
            genre_ids = [g["id"] for g in m["genres"]]
        else:
            genre_ids = m.get("genre_ids", [])

        genres = ", ".join([GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP])
        return poster, year, genres, rating

    except Exception as e:
        print(f"❌ Error for movie_id={movie_id}, title='{title}': {str(e)}")
        return None, "N/A", "N/A", "N/A"


@st.cache_data
def fetch_sentiment_cached(movie_id, api_key):
    return fetch_sentiment(movie_id, api_key)


def render_sentiment_bar(label, pct, color_class):
    st.markdown(
        f'<div class="sent-label">{label} {pct}%</div>'
        f'<div class="sent-bar-wrap"><div class="{color_class}" style="width:{pct}%"></div></div>',
        unsafe_allow_html=True
    )


# ── Page renders immediately; model loads in background ─────────
st.title("🎬 Movie Recommendation System")
st.write("Search a movie you like and get 5 similar movies with posters!")

# Show loading bar only on first load (not cached yet)
with st.spinner("⏳ Loading movie data... (first load only, ~15–20s)"):
    movies_df, new_df, content_sim, collab_sim = get_model()

titles = [""] + movies_df["title"].dropna().tolist()

query = st.selectbox("🔍 Search a movie:", options=titles)
show_sentiment = st.toggle("🧠 Show Sentiment Analysis (NLP)", value=True)

if st.button("Get Recommendations"):
    if not query:
        st.warning("Please select a movie.")
    else:
        results = recommend(query, movies_df, new_df, content_sim, collab_sim)
        if isinstance(results, list) and isinstance(results[0], str) and "not found" in results[0].lower():
            st.error(results[0])
        else:
            with st.spinner("Fetching posters..."):
                movie_details = []
                for r in results:
                    time.sleep(random.uniform(0.8, 1.2))
                    movie_details.append(fetch_movie_details(r["movie_id"], TMDB_API_KEY, title=r["title"]))

            sentiment_data = []
            if show_sentiment:
                with st.spinner("Analysing reviews... 🧠"):
                    for r in results:
                        time.sleep(random.uniform(0.3, 0.6))
                        sentiment_data.append(fetch_sentiment_cached(r["movie_id"], TMDB_API_KEY))
            else:
                sentiment_data = [None] * len(results)

            st.subheader("You might also like:")
            cols = st.columns(5)

            for col, movie, details, sent in zip(cols, results, movie_details, sentiment_data):
                with col:
                    poster, year, genres, rating = details
                    if poster:
                        st.image(poster, width='stretch')
                    else:
                        st.image("https://placehold.co/200x300?text=No+Poster", width='stretch')

                    st.markdown(f"**{movie['title']}**")
                    st.caption(f"⭐ {rating}/10  |  📅 {year}")
                    st.caption(f"🎭 {genres}")
                    st.caption(f"🎬 {movie['director']}")
                    st.caption(f"👥 {movie['cast']}")
                    st.caption(f"🏷️ {movie['keywords']}")

                    mode_icon = "🔀" if movie.get("mode") == "hybrid" else "📐"
                    st.caption(f"{mode_icon} Match score: {movie.get('score', 'N/A')}")

                    if show_sentiment and sent:
                        st.markdown("---")
                        if sent["total"] == 0:
                            st.caption("💬 No reviews found")
                        else:
                            st.caption(f"💬 Reviews: {sent['total']}  |  {sent['label']}")
                            render_sentiment_bar("✅ Positive", sent["pct_pos"], "sent-bar-pos")
                            render_sentiment_bar("❌ Negative", sent["pct_neg"], "sent-bar-neg")
                            render_sentiment_bar("➖ Neutral",  sent["pct_neu"], "sent-bar-neu")

                            if sent["reviews"]:
                                with st.expander("📝 Sample Reviews"):
                                    for rev in sent["reviews"][:3]:
                                        icon = {"positive": "✅", "negative": "❌", "neutral": "➖"}.get(rev["sentiment"], "")
                                        st.markdown(f"{icon} **{rev['author']}**")
                                        st.caption(rev["content"])
                                        st.markdown("---")