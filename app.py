# import streamlit as st
# from recommender import recommend

# st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
# st.title("🎬 Movie Recommendation System")
# st.write("Enter a movie you like and get 5 similar movies!")

# movie_name = st.text_input("Movie Name", placeholder="e.g. Toy Story")

# if st.button("Get Recommendations"):
#     if movie_name.strip() == "":
#         st.warning("Please enter a movie name.")
#     else:
#         results = recommend(movie_name)
#         st.subheader("You might also like:")
#         for i, movie in enumerate(results, 1):
#             st.write(f"{i}. {movie}")



import streamlit as st
import requests
import pandas as pd
import re
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from recommender import recommend
from concurrent.futures import ThreadPoolExecutor
import random

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.markdown("""
    <style>
    [data-testid="stStatusWidget"] { display: none; }
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

def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

@st.cache_data
def fetch_movie_details(title, api_key):
    time.sleep(random.uniform(0.1, 0.4))
    clean_title = re.sub(r'\(\d{4}\)', '', title).strip()
    clean_title = re.sub(r'^(.*),\s*(The|A|An)$', r'\2 \1', clean_title, flags=re.IGNORECASE).strip()
    clean_title = clean_title.strip(',').strip()
    print(f"Searching TMDB for: '{clean_title}'")

    try:
        session = get_session()
        year_match = re.search(r'\((\d{4})\)', title)
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": api_key, "query": clean_title}

        res = session.get(url, params=params, timeout=15).json()
        results = res.get("results", [])

        if results and year_match:
            year_hint = year_match.group(1)
            for r in results:
                if r.get("release_date", "").startswith(year_hint):
                    results[0] = r
                    break

        # if not results:
        #     return None, "N/A", "N/A", "N/A"
        # After your existing results check, before "if not results:"
        if not results or not results[0].get("poster_path"):
            # Fallback: try just first 2 words
            short_title = " ".join(clean_title.split()[:2])
            res2 = session.get(url, params={"api_key": api_key, "query": short_title}, timeout=15).json()
            results2 = res2.get("results", [])
            if results2 and year_match:
                year_hint = year_match.group(1)
                for r in results2:
                    if r.get("release_date", "").startswith(year_hint):
                        results = [r]
                        break
            elif results2:
                results = results2

        m = results[0]
        poster = f"https://image.tmdb.org/t/p/w300{m['poster_path']}" if m.get("poster_path") else None
        year = m.get("release_date", "N/A")[:4]
        rating = round(m.get("vote_average", 0), 1)
        genre_ids = m.get("genre_ids", [])
        genres = ", ".join([GENRE_MAP.get(gid, "") for gid in genre_ids if gid in GENRE_MAP])
        return poster, year, genres, rating

    except Exception as e:
        return None, "N/A", "N/A", "N/A"

# Load titles
movies_df = pd.read_csv("data/movies.csv")
titles = [""] + movies_df["title"].dropna().tolist()

st.title("🎬 Movie Recommendation System")
st.write("Search a movie you like and get 5 similar movies with posters!")

query = st.selectbox("🔍 Search a movie:", options=titles)

if st.button("Get Recommendations"):
    if not query:
        st.warning("Please select a movie.")
    else:
        results = recommend(query)
        if isinstance(results[0], str) and "not found" in results[0].lower():
            st.error(results[0])
        else:
            with st.spinner("Fetching recommendations..."):
                # with ThreadPoolExecutor(max_workers=5) as executor:
                #     movie_details = list(executor.map(lambda m: fetch_movie_details(m, TMDB_API_KEY), results))
                movie_details = []
                for m in results:
                    details = fetch_movie_details(m, TMDB_API_KEY)
                    movie_details.append(details)
                    time.sleep(0.25)

            st.subheader("You might also like:")
            cols = st.columns(5)

            # Fetch all 5 movies in parallel
            with ThreadPoolExecutor(max_workers=5) as executor:
                movie_details = list(executor.map(lambda m: fetch_movie_details(m, TMDB_API_KEY), results))

            for col, movie, details in zip(cols, results, movie_details):
                with col:
                    poster, year, genres, rating = details
                    if poster:
                        st.image(poster, width='stretch')
                    else:
                        st.image("https://placehold.co/200x300?text=No+Poster", width='stretch')
                    st.markdown(f"**{movie}**")
                    st.caption(f"⭐ {rating}/10  |  📅 {year}")
                    st.caption(f"🎭 {genres}")