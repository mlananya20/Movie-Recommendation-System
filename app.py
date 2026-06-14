import streamlit as st
from recommender import recommend

st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
st.title("🎬 Movie Recommendation System")
st.write("Enter a movie you like and get 5 similar movies!")

movie_name = st.text_input("Movie Name", placeholder="e.g. Toy Story")

if st.button("Get Recommendations"):
    if movie_name.strip() == "":
        st.warning("Please enter a movie name.")
    else:
        results = recommend(movie_name)
        st.subheader("You might also like:")
        for i, movie in enumerate(results, 1):
            st.write(f"{i}. {movie}")