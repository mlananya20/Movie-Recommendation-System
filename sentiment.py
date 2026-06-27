# import requests
# import time
# import random
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry

# try:
#     from textblob import TextBlob
#     _USE_TEXTBLOB = True
# except ImportError:
#     _USE_TEXTBLOB = False

# try:
#     import nltk
#     from nltk.sentiment.vader import SentimentIntensityAnalyzer
#     nltk.download("vader_lexicon", quiet=True)
#     _vader = SentimentIntensityAnalyzer()
#     _USE_VADER = True
# except Exception:
#     _USE_VADER = False


# def _get_session():
#     session = requests.Session()
#     retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
#     adapter = HTTPAdapter(max_retries=retry)
#     session.mount("https://", adapter)
#     return session


# def _score_text(text: str) -> str:
#     """Return 'positive', 'negative', or 'neutral' for a piece of text."""
#     if _USE_VADER:
#         scores = _vader.polarity_scores(text)
#         compound = scores["compound"]
#         if compound >= 0.05:
#             return "positive"
#         elif compound <= -0.05:
#             return "negative"
#         else:
#             return "neutral"
#     elif _USE_TEXTBLOB:
#         polarity = TextBlob(text).sentiment.polarity
#         if polarity > 0.05:
#             return "positive"
#         elif polarity < -0.05:
#             return "negative"
#         else:
#             return "neutral"
#     else:
#         # Naive fallback — count positive/negative seed words
#         pos_words = {"great", "excellent", "amazing", "love", "good", "best",
#                      "wonderful", "fantastic", "enjoyed", "brilliant", "fun", "perfect"}
#         neg_words = {"bad", "terrible", "awful", "boring", "worst", "hate",
#                      "disappointed", "poor", "weak", "slow", "waste", "dull"}
#         tokens = set(text.lower().split())
#         pos = len(tokens & pos_words)
#         neg = len(tokens & neg_words)
#         if pos > neg:
#             return "positive"
#         elif neg > pos:
#             return "negative"
#         else:
#             return "neutral"


# def fetch_sentiment(movie_id: int, api_key: str, max_reviews: int = 10) -> dict:
#     """
#     Fetch TMDB reviews for movie_id and return sentiment breakdown.

#     Returns:
#         {
#             "positive": int,
#             "negative": int,
#             "neutral":  int,
#             "total":    int,
#             "pct_pos":  float,   # 0–100
#             "pct_neg":  float,
#             "pct_neu":  float,
#             "label":    str,     # "Mostly Positive" / "Mixed" / "Mostly Negative" / "No Reviews"
#             "reviews":  list[dict]   # [{author, content, sentiment}, ...]
#         }
#     """
#     empty = {
#         "positive": 0, "negative": 0, "neutral": 0,
#         "total": 0, "pct_pos": 0.0, "pct_neg": 0.0, "pct_neu": 0.0,
#         "label": "No Reviews", "reviews": []
#     }

#     try:
#         time.sleep(random.uniform(0.1, 0.3))
#         session = _get_session()
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"
#         resp = session.get(url, params={"api_key": api_key, "language": "en-US", "page": 1}, timeout=15)
#         if resp.status_code != 200:
#             return empty

#         data = resp.json()
#         raw_reviews = data.get("results", [])[:max_reviews]

#         if not raw_reviews:
#             return empty

#         counts = {"positive": 0, "negative": 0, "neutral": 0}
#         enriched = []

#         for rev in raw_reviews:
#             content = rev.get("content", "")
#             if not content:
#                 continue
#             sentiment = _score_text(content)
#             counts[sentiment] += 1
#             enriched.append({
#                 "author":    rev.get("author", "Anonymous"),
#                 "content":   content[:300],   # truncate for display
#                 "sentiment": sentiment,
#             })

#         total = sum(counts.values())
#         if total == 0:
#             return empty

#         pct_pos = round(counts["positive"] / total * 100, 1)
#         pct_neg = round(counts["negative"] / total * 100, 1)
#         pct_neu = round(counts["neutral"]  / total * 100, 1)

#         if pct_pos >= 60:
#             label = "😊 Mostly Positive"
#         elif pct_neg >= 60:
#             label = "😞 Mostly Negative"
#         elif pct_pos >= 40:
#             label = "😐 Mixed"
#         else:
#             label = "😐 Mixed"

#         return {
#             "positive": counts["positive"],
#             "negative": counts["negative"],
#             "neutral":  counts["neutral"],
#             "total":    total,
#             "pct_pos":  pct_pos,
#             "pct_neg":  pct_neg,
#             "pct_neu":  pct_neu,
#             "label":    label,
#             "reviews":  enriched,
#         }

#     except Exception as e:
#         print(f"❌ Sentiment fetch error for movie_id={movie_id}: {e}")
#         return empty

import requests
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    from textblob import TextBlob
    _USE_TEXTBLOB = True
except ImportError:
    _USE_TEXTBLOB = False

try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    nltk.download("vader_lexicon", quiet=True)
    _vader = SentimentIntensityAnalyzer()
    _USE_VADER = True
except Exception:
    _USE_VADER = False


def _get_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=2,                          # 2s, 4s, 8s, 16s gaps
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def _score_text(text: str) -> str:
    """Return 'positive', 'negative', or 'neutral' for a piece of text."""
    if _USE_VADER:
        scores = _vader.polarity_scores(text)
        compound = scores["compound"]
        if compound >= 0.05:
            return "positive"
        elif compound <= -0.05:
            return "negative"
        else:
            return "neutral"
    elif _USE_TEXTBLOB:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.05:
            return "positive"
        elif polarity < -0.05:
            return "negative"
        else:
            return "neutral"
    else:
        # Naive fallback — count positive/negative seed words
        pos_words = {"great", "excellent", "amazing", "love", "good", "best",
                     "wonderful", "fantastic", "enjoyed", "brilliant", "fun", "perfect"}
        neg_words = {"bad", "terrible", "awful", "boring", "worst", "hate",
                     "disappointed", "poor", "weak", "slow", "waste", "dull"}
        tokens = set(text.lower().split())
        pos = len(tokens & pos_words)
        neg = len(tokens & neg_words)
        if pos > neg:
            return "positive"
        elif neg > pos:
            return "negative"
        else:
            return "neutral"


def fetch_sentiment(movie_id: int, api_key: str, max_reviews: int = 10) -> dict:
    """
    Fetch TMDB reviews for movie_id and return sentiment breakdown.

    Returns:
        {
            "positive": int,
            "negative": int,
            "neutral":  int,
            "total":    int,
            "pct_pos":  float,   # 0–100
            "pct_neg":  float,
            "pct_neu":  float,
            "label":    str,     # "Mostly Positive" / "Mixed" / "Mostly Negative" / "No Reviews"
            "reviews":  list[dict]   # [{author, content, sentiment}, ...]
        }
    """
    empty = {
        "positive": 0, "negative": 0, "neutral": 0,
        "total": 0, "pct_pos": 0.0, "pct_neg": 0.0, "pct_neu": 0.0,
        "label": "No Reviews", "reviews": []
    }

    try:
        # Longer delay — sentiment calls follow poster fetches, TMDB needs breathing room
        time.sleep(random.uniform(1.0, 1.8))
        session = _get_session()
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"

        # Manual retry for ConnectionResetError (10054) — not caught by urllib3 Retry
        resp = None
        for attempt in range(4):
            try:
                resp = session.get(
                    url,
                    params={"api_key": api_key, "language": "en-US", "page": 1},
                    timeout=20,
                )
                break
            except Exception as conn_err:
                if attempt < 3:
                    wait = 2 ** (attempt + 1) + random.uniform(0, 1)
                    print(f"\u26a0\ufe0f Sentiment conn error (attempt {attempt+1}), retrying in {wait:.1f}s: {conn_err}")
                    time.sleep(wait)
                else:
                    raise

        if resp is None or resp.status_code != 200:
            return empty

        data = resp.json()
        raw_reviews = data.get("results", [])[:max_reviews]

        if not raw_reviews:
            return empty

        counts = {"positive": 0, "negative": 0, "neutral": 0}
        enriched = []

        for rev in raw_reviews:
            content = rev.get("content", "")
            if not content:
                continue
            sentiment = _score_text(content)
            counts[sentiment] += 1
            enriched.append({
                "author":    rev.get("author", "Anonymous"),
                "content":   content[:300],   # truncate for display
                "sentiment": sentiment,
            })

        total = sum(counts.values())
        if total == 0:
            return empty

        pct_pos = round(counts["positive"] / total * 100, 1)
        pct_neg = round(counts["negative"] / total * 100, 1)
        pct_neu = round(counts["neutral"]  / total * 100, 1)

        if pct_pos >= 60:
            label = "😊 Mostly Positive"
        elif pct_neg >= 60:
            label = "😞 Mostly Negative"
        elif pct_pos >= 40:
            label = "😐 Mixed"
        else:
            label = "😐 Mixed"

        return {
            "positive": counts["positive"],
            "negative": counts["negative"],
            "neutral":  counts["neutral"],
            "total":    total,
            "pct_pos":  pct_pos,
            "pct_neg":  pct_neg,
            "pct_neu":  pct_neu,
            "label":    label,
            "reviews":  enriched,
        }

    except Exception as e:
        print(f"❌ Sentiment fetch error for movie_id={movie_id}: {e}")
        return empty