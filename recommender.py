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
    # matches = movies[movies["title"].str.contains(movie_name, case=False, na=False)]
    matches = movies[movies["title"].str.contains(movie_name, case=False, na=False, regex=False)]
    
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

