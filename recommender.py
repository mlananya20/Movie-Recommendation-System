# # import pandas as pd
# # from sklearn.feature_extraction.text import CountVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity

# # # Load data
# # movies = pd.read_csv("data/movies.csv")
# # movies["genres"] = movies["genres"].fillna("").str.replace("|", " ")

# # # Build similarity matrix
# # cv = CountVectorizer(stop_words="english")
# # genre_matrix = cv.fit_transform(movies["genres"])
# # similarity = cosine_similarity(genre_matrix)

# # # Recommendation function
# # def recommend(movie_name):
# #     # matches = movies[movies["title"].str.contains(movie_name, case=False, na=False)]
# #     matches = movies[movies["title"].str.contains(movie_name, case=False, na=False, regex=False)]
    
# #     if matches.empty:
# #         return ["Movie not found. Try another title."]
    
# #     movie_index = matches.index[0]
# #     distances = similarity[movie_index]
    
# #     movie_list = sorted(
# #         list(enumerate(distances)),
# #         reverse=True,
# #         key=lambda x: x[1]
# #     )[1:6]
    
# #     return [movies.iloc[i[0]].title for i in movie_list]


# import pandas as pd
# import ast
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load datasets
# movies = pd.read_csv("data/tmdb_5000_movies.csv")
# credits = pd.read_csv("data/tmdb_5000_credits.csv")

# # Merge datasets
# movies = movies.merge(credits, on="title")

# # Keep useful columns
# movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# movies.dropna(inplace=True)

# # ---------- Helper Functions ----------

# def convert(text):
#     L = []
#     for i in ast.literal_eval(text):
#         L.append(i['name'])
#     return L

# def convert3(text):
#     L = []
#     counter = 0
#     for i in ast.literal_eval(text):
#         if counter != 3:
#             L.append(i['name'])
#             counter += 1
#         else:
#             break
#     return L

# def fetch_director(text):
#     L = []
#     for i in ast.literal_eval(text):
#         if i['job'] == 'Director':
#             L.append(i['name'])
#             break
#     return L

# # ---------- Feature Engineering ----------

# movies['genres'] = movies['genres'].apply(convert)
# movies['keywords'] = movies['keywords'].apply(convert)
# movies['cast'] = movies['cast'].apply(convert3)
# movies['crew'] = movies['crew'].apply(fetch_director)

# movies['keywords_display'] = movies['keywords'].apply(lambda x: x[:4])  # ← BEFORE space removal
# movies['cast_display'] = movies['cast'].apply(lambda x: x[:3])          # ← BEFORE space removal

# movies['overview'] = movies['overview'].apply(lambda x: x.split())

# movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
# movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
# movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
# movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

# movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# # new_df = movies[['movie_id','title','tags']]
# new_df = movies[['movie_id','title','tags']].copy()

# new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
# new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# # ---------- Vectorization ----------

# cv = CountVectorizer(max_features=5000, stop_words='english')

# vectors = cv.fit_transform(new_df['tags']).toarray()

# similarity = cosine_similarity(vectors)

# # ---------- Recommendation ----------

# # def recommend(movie_name):
# #     matches = new_df[new_df["title"].str.contains(movie_name, case=False, na=False, regex=False)]

# #     if matches.empty:
# #         return ["Movie not found"]

# #     movie_index = matches.index[0]

# #     distances = similarity[movie_index]

# #     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

# #     #return [new_df.iloc[i[0]].title for i in movie_list]
# #     return [(new_df.iloc[i[0]].movie_id, new_df.iloc[i[0]].title) for i in movie_list]

# def recommend(movie_name):
#     matches = new_df[new_df["title"].str.contains(movie_name, case=False, na=False, regex=False)]

#     if matches.empty:
#         return ["Movie not found"]

#     movie_index = matches.index[0]
#     distances = similarity[movie_index]
#     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     results = []
#     for i in movie_list:
#         row = movies.iloc[i[0]]  # use full movies df, not new_df
#         results.append({
#             "movie_id": row["movie_id"],
#             "title":    row["title"],
#             "director": ", ".join(row["crew"]) if row["crew"] else "N/A",
#             # "cast":     ", ".join(row["cast"][:3]) if row["cast"] else "N/A",
#             # "keywords": ", ".join(row["keywords"][:4]) if row["keywords"] else "N/A",
#             "cast":     ", ".join(row["cast_display"]) if row["cast_display"] else "N/A",
#             "keywords": ", ".join(row["keywords_display"]) if row["keywords_display"] else "N/A",
#         })
#     return results

import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# ── Load datasets ────────────────────────────────────────────────
movies  = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")
movies  = movies.merge(credits, on="title")
movies  = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)

# ── Helpers ──────────────────────────────────────────────────────
def convert(text):
    return [i['name'] for i in ast.literal_eval(text)]

def convert3(text):
    return [i['name'] for i in ast.literal_eval(text)][:3]

def fetch_director(text):
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            return [i['name']]
    return []

# ── Feature engineering ──────────────────────────────────────────
movies['genres']   = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast']     = movies['cast'].apply(convert3)
movies['crew']     = movies['crew'].apply(fetch_director)

movies['keywords_display'] = movies['keywords'].apply(lambda x: x[:4])
movies['cast_display']     = movies['cast'].apply(lambda x: x[:3])

movies['overview']  = movies['overview'].apply(lambda x: x.split())
movies['genres']    = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords']  = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast']      = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew']      = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['tags']      = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['movie_id', 'title', 'tags']].copy()
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x)).str.lower()

# ── Content-based similarity ─────────────────────────────────────
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors    = cv.fit_transform(new_df['tags']).toarray()
content_sim = cosine_similarity(vectors)   # shape: (n_movies, n_movies)

# ── Collaborative filtering ──────────────────────────────────────
collab_sim = None

RATINGS_PATH = "data/ratings.csv"   # userId, movieId, rating, timestamp (MovieLens format)

if os.path.exists(RATINGS_PATH):
    ratings = pd.read_csv(RATINGS_PATH)

    # Keep only movies that exist in our TMDB dataset
    valid_ids = set(movies['movie_id'].tolist())
    ratings   = ratings[ratings['movieId'].isin(valid_ids)]

    if not ratings.empty:
        # Build user-movie matrix (rows=users, cols=movies)
        user_movie = ratings.pivot_table(
            index='userId', columns='movieId', values='rating'
        ).fillna(0)

        # Align columns to match new_df order
        aligned_ids = [mid for mid in new_df['movie_id'].tolist() if mid in user_movie.columns]
        user_movie  = user_movie[aligned_ids]

        # Movie-movie collaborative similarity
        movie_matrix = user_movie.T   # rows=movies, cols=users
        collab_sim_partial = cosine_similarity(movie_matrix)

        # Map back to full index of new_df
        collab_df = pd.DataFrame(
            collab_sim_partial,
            index=aligned_ids,
            columns=aligned_ids
        )

        # Build full matrix (same size as content_sim), default 0
        n = len(new_df)
        collab_sim = [[0.0] * n for _ in range(n)]
        id_to_idx  = {mid: idx for idx, mid in enumerate(new_df['movie_id'].tolist())}

        for i, mid_i in enumerate(aligned_ids):
            for j, mid_j in enumerate(aligned_ids):
                r = id_to_idx.get(mid_i)
                c = id_to_idx.get(mid_j)
                if r is not None and c is not None:
                    collab_sim[r][c] = float(collab_df.iloc[i, j])

        import numpy as np
        collab_sim = np.array(collab_sim)
        print(f"✅ Collaborative filtering loaded: {len(aligned_ids)} movies with ratings")
    else:
        print("⚠️ ratings.csv has no overlap with TMDB movies — using content-only")
else:
    print("⚠️ data/ratings.csv not found — using content-only mode")


# ── Hybrid recommend ─────────────────────────────────────────────
def recommend(movie_name, content_weight=0.6, collab_weight=0.4):
    matches = new_df[new_df["title"].str.contains(movie_name, case=False, na=False, regex=False)]
    if matches.empty:
        return ["Movie not found"]

    movie_index = matches.index[0]

    if collab_sim is not None:
        hybrid = (content_weight * content_sim[movie_index]) + \
                 (collab_weight  * collab_sim[movie_index])
    else:
        hybrid = content_sim[movie_index]

    movie_list = sorted(list(enumerate(hybrid)), reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for i, score in movie_list:
        row = movies.iloc[i]
        results.append({
            "movie_id": row["movie_id"],
            "title":    row["title"],
            "director": ", ".join(row["crew"])          if row["crew"]             else "N/A",
            "cast":     ", ".join(row["cast_display"])  if row["cast_display"]     else "N/A",
            "keywords": ", ".join(row["keywords_display"]) if row["keywords_display"] else "N/A",
            "score":    round(float(score), 4),
            "mode":     "hybrid" if collab_sim is not None else "content",
        })
    return results