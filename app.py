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

# import streamlit as st
# from recommender import recommend, search_suggestions

# # ── Page config ───────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Movie Recommender",
#     page_icon="🎬",
#     layout="wide",
# )

# st.title("🎬 Movie Recommendation System")
# st.write("Type a movie title below and get 5 similar picks — with posters, ratings, and details!")

# # ── Search with suggestions ───────────────────────────────────────────────────
# query = st.text_input("🔍 Start typing a movie name...", placeholder="e.g. Interstellar")

# selected_title = None
# if query and len(query) >= 2:
#     suggestions = search_suggestions(query)
#     if suggestions:
#         selected_title = st.selectbox(
#             "Select a movie from the list:",
#             options=suggestions,
#             index=0,
#         )
#     else:
#         st.caption("No matching titles found — try a different spelling.")

# # ── Recommend button ──────────────────────────────────────────────────────────
# if st.button("🎯 Get Recommendations", use_container_width=True):
#     if not selected_title:
#         st.warning("Please type a movie name and select from the suggestions.")
#     else:
#         with st.spinner("Fetching recommendations and posters..."):
#             selected, recs = recommend(selected_title)

#         if selected is None:
#             st.error("Movie not found. Try a different title.")
#         else:
#             # ── Selected movie card ───────────────────────────────────────────
#             st.markdown("---")
#             st.subheader("🎥 You selected:")
#             col_poster, col_info = st.columns([1, 3])

#             with col_poster:
#                 if selected.get("poster"):
#                     st.image(selected["poster"], width=200)
#                 else:
#                     st.image("https://via.placeholder.com/200x300?text=No+Poster", width=200)

#             with col_info:
#                 year_str = f"({selected['year']})" if selected.get("year") else ""
#                 st.markdown(f"## {selected['title']} {year_str}")
#                 rating = selected.get("rating", 0)
#                 if rating:
#                     st.markdown(f"⭐ **IMDb Rating:** {rating} / 10")
#                 if selected.get("genres"):
#                     st.markdown(f"🎭 **Genres:** {selected['genres']}")
#                 if selected.get("overview"):
#                     st.markdown(f"📖 **Overview:** {selected['overview']}")

#             # ── Recommendations grid ──────────────────────────────────────────
#             st.markdown("---")
#             st.subheader("🍿 You might also like:")

#             if not recs:
#                 st.info("No recommendations found.")
#             else:
#                 cols = st.columns(len(recs))
#                 for col, movie in zip(cols, recs):
#                     with col:
#                         if movie.get("poster"):
#                             st.image(movie["poster"], use_column_width=True)
#                         else:
#                             st.image(
#                                 "https://via.placeholder.com/200x300?text=No+Poster",
#                                 use_column_width=True,
#                             )
#                         year_str = f"({movie['year']})" if movie.get("year") else ""
#                         st.markdown(f"**{movie['title']}** {year_str}")
#                         rating = movie.get("rating", 0)
#                         if rating:
#                             st.markdown(f"⭐ {rating}")
#                         if movie.get("genres"):
#                             # Show first 2 genres to keep it compact
#                             genres_short = " · ".join(movie["genres"].split(" · ")[:2])
#                             st.caption(genres_short)
#                         if movie.get("overview"):
#                             with st.expander("Overview"):
#                                 st.write(movie["overview"])

# # ── Footer ─────────────────────────────────────────────────────────────────────
# st.markdown("---")
# st.caption("Powered by MovieLens data + TMDB API · Built with Streamlit")