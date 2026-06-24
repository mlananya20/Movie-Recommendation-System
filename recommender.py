import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
movies = pd.read_csv("data/movies.csv")
movies["genres"] = movies["genres"].fillna("").str.replace("|", " ")

# Build similarity matrix
cv = CountVectorizer(stop_words="english")
genre_matrix = cv.fit_transform(movies["genres"])
similarity = cosine_similarity(genre_matrix)

# Recommendation function
def recommend(movie_name):
    matches = movies[movies["title"].str.contains(movie_name, case=False, na=False)]
    
    if matches.empty:
        return ["Movie not found. Try another title."]
    
    movie_index = matches.index[0]
    distances = similarity[movie_index]
    
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
    
    return [movies.iloc[i[0]].title for i in movie_list]


# import os
# import requests
# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from dotenv import load_dotenv

# load_dotenv()
# TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# TMDB_BASE = "https://api.themoviedb.org/3"
# POSTER_BASE = "https://image.tmdb.org/t/p/w500"

# # ── Load & prep data ──────────────────────────────────────────────────────────
# movies = pd.read_csv("data/movies.csv")
# movies["genres_clean"] = movies["genres"].fillna("").str.replace("|", " ", regex=False)

# # Extract year from title like "Toy Story (1995)" → 1995
# movies["year"] = movies["title"].str.extract(r"\((\d{4})\)$")
# movies["title_clean"] = movies["title"].str.replace(r"\s*\(\d{4}\)$", "", regex=True).str.strip()

# # ── Build similarity matrix ───────────────────────────────────────────────────
# cv = CountVectorizer(stop_words="english")
# genre_matrix = cv.fit_transform(movies["genres_clean"])
# similarity = cosine_similarity(genre_matrix)


# # ── TMDB helpers ──────────────────────────────────────────────────────────────
# def fetch_tmdb_details(title: str, year: str = None) -> dict:
#     """Search TMDB for a movie and return details + poster URL."""
#     if not TMDB_API_KEY:
#         return {}
#     try:
#         params = {"api_key": TMDB_API_KEY, "query": title, "language": "en-US"}
#         if year:
#             params["year"] = year
#         r = requests.get(f"{TMDB_BASE}/search/movie", params=params, timeout=5)
#         r.raise_for_status()
#         results = r.json().get("results", [])
#         if not results:
#             return {}
#         m = results[0]
#         poster = f"{POSTER_BASE}{m['poster_path']}" if m.get("poster_path") else None
#         return {
#             "poster": poster,
#             "rating": round(m.get("vote_average", 0), 1),
#             "overview": m.get("overview", "No overview available."),
#             "release_date": m.get("release_date", ""),
#             "tmdb_id": m.get("id"),
#         }
#     except Exception:
#         return {}


# # ── Main recommendation function ──────────────────────────────────────────────
# def recommend(movie_name: str, n: int = 5):
#     """
#     Returns the input movie's info + a list of n recommended movies,
#     each with TMDB details attached.

#     Returns:
#         selected: dict  – info about the movie the user typed
#         recs:     list  – list of dicts for recommended movies
#     """
#     matches = movies[movies["title"].str.contains(movie_name, case=False, na=False)]
#     if matches.empty:
#         return None, []

#     # Pick the first match
#     idx = matches.index[0]
#     row = movies.loc[idx]

#     # Fetch TMDB details for the selected movie
#     selected_tmdb = fetch_tmdb_details(row["title_clean"], row["year"])
#     selected = {
#         "title": row["title_clean"],
#         "year": row.get("year", ""),
#         "genres": row["genres"].replace("|", " · "),
#         **selected_tmdb,
#     }

#     # Compute similarities
#     distances = list(enumerate(similarity[idx]))
#     distances.sort(key=lambda x: x[1], reverse=True)
#     top_indices = [i for i, _ in distances[1 : n + 6]]  # grab a few extra in case of dups

#     recs = []
#     seen_titles = set()
#     for i in top_indices:
#         r = movies.iloc[i]
#         clean = r["title_clean"]
#         if clean in seen_titles:
#             continue
#         seen_titles.add(clean)
#         tmdb = fetch_tmdb_details(clean, r["year"])
#         recs.append({
#             "title": clean,
#             "year": r.get("year", ""),
#             "genres": r["genres"].replace("|", " · "),
#             **tmdb,
#         })
#         if len(recs) == n:
#             break

#     return selected, recs


# # ── Search suggestions ────────────────────────────────────────────────────────
# def search_suggestions(query: str, limit: int = 8) -> list[str]:
#     """Return movie titles that match the typed query (for the selectbox)."""
#     if not query or len(query) < 2:
#         return []
#     mask = movies["title"].str.contains(query, case=False, na=False)
#     return movies.loc[mask, "title"].head(limit).tolist()