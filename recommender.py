# import pandas as pd
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load data
# movies = pd.read_csv("data/movies.csv")
# movies["genres"] = movies["genres"].fillna("").str.replace("|", " ")

# # Build similarity matrix
# cv = CountVectorizer(stop_words="english")
# genre_matrix = cv.fit_transform(movies["genres"])
# similarity = cosine_similarity(genre_matrix)

# # Recommendation function
# def recommend(movie_name):
#     # matches = movies[movies["title"].str.contains(movie_name, case=False, na=False)]
#     matches = movies[movies["title"].str.contains(movie_name, case=False, na=False, regex=False)]
    
#     if matches.empty:
#         return ["Movie not found. Try another title."]
    
#     movie_index = matches.index[0]
#     distances = similarity[movie_index]
    
#     movie_list = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]
    
#     return [movies.iloc[i[0]].title for i in movie_list]


import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Merge datasets
movies = movies.merge(credits, on="title")

# Keep useful columns
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

movies.dropna(inplace=True)

# ---------- Helper Functions ----------

def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

def convert3(text):
    L = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break
    return L

def fetch_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
            break
    return L

# ---------- Feature Engineering ----------

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

movies['keywords_display'] = movies['keywords'].apply(lambda x: x[:4])  # ← BEFORE space removal
movies['cast_display'] = movies['cast'].apply(lambda x: x[:3])          # ← BEFORE space removal

movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# new_df = movies[['movie_id','title','tags']]
new_df = movies[['movie_id','title','tags']].copy()

new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# ---------- Vectorization ----------

cv = CountVectorizer(max_features=5000, stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()

similarity = cosine_similarity(vectors)

# ---------- Recommendation ----------

# def recommend(movie_name):
#     matches = new_df[new_df["title"].str.contains(movie_name, case=False, na=False, regex=False)]

#     if matches.empty:
#         return ["Movie not found"]

#     movie_index = matches.index[0]

#     distances = similarity[movie_index]

#     movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

#     #return [new_df.iloc[i[0]].title for i in movie_list]
#     return [(new_df.iloc[i[0]].movie_id, new_df.iloc[i[0]].title) for i in movie_list]

def recommend(movie_name):
    matches = new_df[new_df["title"].str.contains(movie_name, case=False, na=False, regex=False)]

    if matches.empty:
        return ["Movie not found"]

    movie_index = matches.index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for i in movie_list:
        row = movies.iloc[i[0]]  # use full movies df, not new_df
        results.append({
            "movie_id": row["movie_id"],
            "title":    row["title"],
            "director": ", ".join(row["crew"]) if row["crew"] else "N/A",
            # "cast":     ", ".join(row["cast"][:3]) if row["cast"] else "N/A",
            # "keywords": ", ".join(row["keywords"][:4]) if row["keywords"] else "N/A",
            "cast":     ", ".join(row["cast_display"]) if row["cast_display"] else "N/A",
            "keywords": ", ".join(row["keywords_display"]) if row["keywords_display"] else "N/A",
        })
    return results