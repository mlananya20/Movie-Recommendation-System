
import streamlit as st
import requests
import re
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from recommender import load_model, recommend
from sentiment import fetch_sentiment
from chatbot import init_gemini, parse_user_intent, generate_chat_response
from dotenv import load_dotenv
import os

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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

GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV Movie",
    53: "Thriller", 10752: "War", 37: "Western"
}


@st.cache_resource(show_spinner=False)
def get_model():
    return load_model()


@st.cache_resource(show_spinner=False)
def get_gemini():
    return init_gemini(GEMINI_API_KEY)


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


# ── Page title ───────────────────────────────────────────────────
st.title("🎬 Movie Recommendation System")

with st.spinner("⏳ Loading movie data... (first load only, ~15–20s)"):
    movies_df, new_df, content_sim, collab_sim = get_model()

tab1, tab2 = st.tabs(["🔍 Search by Movie", "🤖 AI Chatbot"])


# ════════════════════════════════════════════════════════════════
# TAB 1 — Original Search
# ════════════════════════════════════════════════════════════════
with tab1:
    st.write("Search a movie you like and get 5 similar movies with posters!")

    titles = [""] + movies_df["title"].dropna().tolist()
    query = st.selectbox("🔍 Search a movie:", options=titles, key="tab1_search")
    show_sentiment = st.toggle("🧠 Show Sentiment Analysis (NLP)", value=True, key="tab1_sentiment")

    if st.button("Get Recommendations", key="tab1_btn"):
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


# ════════════════════════════════════════════════════════════════
# TAB 2 — AI Chatbot
# ════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🤖 Chat with AI Movie Assistant")
    st.caption("Try: 'I want a thrilling sci-fi movie' or 'Something funny like The Hangover'")

    gemini_model = get_gemini()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg.get("movies"):
                cols = st.columns(5)
                for col, movie in zip(cols, msg["movies"]):
                    with col:
                        if movie.get("poster"):
                            st.image(movie["poster"], width=120)
                        st.caption(f"**{movie['title']}**")
                        st.caption(f"⭐ {movie['rating']} | 📅 {movie['year']}")

    user_input = st.chat_input("Ask me for a movie recommendation...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                intent = parse_user_intent(gemini_model, user_input)
                search_query = intent.get("search_query", "")

                if intent.get("error") == "quota":
                    reply = "⏳ Gemini API is rate-limited right now. Please wait 1 minute and try again!"
                    st.warning(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply, "movies": []})
                elif not search_query:
                    reply = "I couldn't understand your request. Try something like 'I want a scary horror movie'!"
                    st.write(reply)
                    st.session_state.chat_history.append({
                        "role": "assistant", "content": reply, "movies": []
                    })
                else:
                    results = recommend(search_query, movies_df, new_df, content_sim, collab_sim)

                    if isinstance(results, list) and isinstance(results[0], str):
                        reply = f"Gemini suggested **'{search_query}'** but I couldn't find it in my database. Try being more specific!"
                        st.write(reply)
                        st.session_state.chat_history.append({
                            "role": "assistant", "content": reply, "movies": []
                        })
                    else:
                        chat_movies = []
                        for r in results:
                            poster, year, genres, rating = fetch_movie_details(
                                r["movie_id"], TMDB_API_KEY, r["title"]
                            )
                            chat_movies.append({
                                "title":  r["title"],
                                "poster": poster,
                                "year":   year,
                                "rating": rating,
                            })

                        reply = generate_chat_response(gemini_model, user_input, results)
                        st.write(reply)

                        cols = st.columns(5)
                        for col, movie in zip(cols, chat_movies):
                            with col:
                                if movie.get("poster"):
                                    st.image(movie["poster"], width=120)
                                st.caption(f"**{movie['title']}**")
                                st.caption(f"⭐ {movie['rating']} | 📅 {movie['year']}")

                        st.session_state.chat_history.append({
                            "role":    "assistant",
                            "content": reply,
                            "movies":  chat_movies,
                        })