# import google.generativeai as genai
# import json
# import re

# def init_gemini(api_key: str):
#     genai.configure(api_key=api_key)
#     return genai.GenerativeModel("gemini-2.0-flash")

# def parse_user_intent(model, user_message: str) -> dict:
#     """
#     Send user's natural language to Gemini.
#     Returns a dict with: search_query, genres, mood, explanation
#     """
#     prompt = f"""
# You are a movie recommendation assistant. A user said: "{user_message}"

# Extract what kind of movie they want and return ONLY a valid JSON object with these fields:
# {{
#   "search_query": "a specific movie title that best matches their request (pick one well-known movie)",
#   "genres": ["list", "of", "genres"],
#   "mood": "one word mood like thrilling/funny/emotional/scary",
#   "explanation": "one sentence explaining why you picked this movie"
# }}

# Rules:
# - search_query must be a real, well-known movie title from TMDB
# - If they mention a specific movie, use that as search_query
# - If they describe a mood/genre, pick the most iconic movie for that
# - Return ONLY the JSON, no extra text, no markdown
# """
#     response = model.generate_content(prompt)
#     text = response.text.strip()
    
#     # Clean up if Gemini adds markdown
#     text = re.sub(r"```json|```", "", text).strip()
    
#     try:
#         return json.loads(text)
#     except json.JSONDecodeError:
#         # Fallback if parsing fails
#         return {
#             "search_query": "",
#             "genres": [],
#             "mood": "interesting",
#             "explanation": "Based on your request, here are some recommendations."
#         }

# def generate_chat_response(model, user_message: str, recommended_movies: list) -> str:
#     """
#     After getting recommendations, generate a friendly chat response.
#     """
#     movie_titles = [m["title"] for m in recommended_movies]
    
#     prompt = f"""
# You are a friendly movie recommendation chatbot. 
# The user asked: "{user_message}"
# You found these movies for them: {movie_titles}

# Write a short, enthusiastic 2-3 sentence response telling them about these picks.
# Be conversational, mention why these fit their request. No bullet points.
# """
#     response = model.generate_content(prompt)
#     return response.text.strip()




# import google.generativeai as genai
# import json
# import re
# import time

# def init_gemini(api_key: str):
#     genai.configure(api_key=api_key)
#     # return genai.GenerativeModel("gemini-2.0-flash")
#     return genai.GenerativeModel("gemini-1.5-flash-latest")

# def parse_user_intent(model, user_message: str) -> dict:
#     prompt = f"""
# You are a movie recommendation assistant. A user said: "{user_message}"

# Extract what kind of movie they want and return ONLY a valid JSON object:
# {{
#   "search_query": "a specific well-known movie title that best matches their request",
#   "genres": ["list", "of", "genres"],
#   "mood": "one word mood",
#   "explanation": "one sentence why you picked this movie"
# }}

# Rules:
# - search_query must be a real, well-known movie title
# - If they mention a specific movie, use that
# - If they describe mood/genre, pick the most iconic movie for it
# - Return ONLY the JSON, no extra text, no markdown backticks
# """
#     # Retry up to 3 times with 60s wait on quota error
#     for attempt in range(3):
#         try:
#             response = model.generate_content(prompt)
#             text = re.sub(r"```json|```", "", response.text.strip()).strip()
#             return json.loads(text)
#         except Exception as e:
#             err = str(e)
#             if "429" in err or "quota" in err.lower():
#                 if attempt < 2:
#                     time.sleep(60)  # wait 1 minute and retry
#                     continue
#                 else:
#                     return {"search_query": "", "error": "quota"}
#             else:
#                 return {"search_query": "", "error": str(e)}
#     return {"search_query": "", "error": "quota"}

# def generate_chat_response(model, user_message: str, recommended_movies: list) -> str:
#     titles = [m["title"] for m in recommended_movies]
#     prompt = f"""
# You are a friendly movie recommendation chatbot.
# User asked: "{user_message}"
# You found these movies: {titles}

# Write a short enthusiastic 2-3 sentence response explaining why these fit their request.
# Be conversational, no bullet points.
# """
#     for attempt in range(3):
#         try:
#             return model.generate_content(prompt).text.strip()
#         except Exception as e:
#             err = str(e)
#             if "429" in err or "quota" in err.lower():
#                 if attempt < 2:
#                     time.sleep(60)
#                     continue
#                 else:
#                     return f"Here are some great movies that match your request: {', '.join(titles)}"
#             else:
#                 return f"Here are some great movies that match your request: {', '.join(titles)}"
#     return f"Here are some movies for you: {', '.join(titles)}"




# import google.generativeai as genai
# import json
# import re
# import time

# def init_gemini(api_key: str):
#     genai.configure(api_key=api_key)
#     # return genai.GenerativeModel("gemini-2.0-flash")
#     return genai.GenerativeModel("gemini-1.5-flash-latest")

# def parse_user_intent(model, user_message: str) -> dict:
#     prompt = f"""You are a movie recommendation assistant.

# A user said: "{user_message}"

# Reply with ONLY this JSON and nothing else:
# {{"search_query": "Inception", "genres": ["Sci-Fi", "Thriller"], "mood": "mind-bending", "explanation": "Inception is the most iconic mind-bending sci-fi movie."}}

# Replace the values based on what the user wants. search_query must be a real famous movie title. No markdown, no backticks, just raw JSON."""

#     for attempt in range(3):
#         try:
#             response = model.generate_content(prompt)
#             raw = response.text.strip()
#             # Clean any markdown if present
#             raw = re.sub(r"```json|```", "", raw).strip()
#             # Find JSON object in response
#             match = re.search(r'\{.*\}', raw, re.DOTALL)
#             if match:
#                 return json.loads(match.group())
#             return {"search_query": "Inception", "genres": ["Sci-Fi"], "mood": "thrilling", "explanation": "Default pick"}
#         except Exception as e:
#             err = str(e)
#             if "429" in err or "quota" in err.lower():
#                 if attempt < 2:
#                     time.sleep(5)
#                     continue
#                 return {"search_query": "", "error": "quota"}
#             return {"search_query": "Inception", "genres": ["Sci-Fi"], "mood": "thrilling", "explanation": "Default pick"}
#     return {"search_query": "", "error": "quota"}

# def generate_chat_response(model, user_message: str, recommended_movies: list) -> str:
#     titles = [m["title"] for m in recommended_movies]
#     prompt = f"""You are a friendly movie chatbot. User asked: "{user_message}". You found: {titles}. Write 2-3 enthusiastic sentences about why these movies fit. No bullet points."""

#     for attempt in range(3):
#         try:
#             return model.generate_content(prompt).text.strip()
#         except Exception as e:
#             err = str(e)
#             if "429" in err or "quota" in err.lower():
#                 if attempt < 2:
#                     time.sleep(5)
#                     continue
#             return f"Great picks for you: {', '.join(titles)}!"
#     return f"Here are some movies for you: {', '.join(titles)}"






import google.generativeai as genai
import json
import re

def init_gemini(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-latest")

def parse_user_intent(model, user_message: str) -> dict:
    prompt = f"""User wants a movie: "{user_message}"
Reply with ONLY raw JSON, no markdown:
{{"search_query": "Inception"}}
Replace Inception with the best matching real movie title."""

    try:
        response = model.generate_content(prompt)
        raw = re.sub(r"```json|```", "", response.text.strip()).strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return {"search_query": data.get("search_query", "Inception")}
    except Exception as e:
        if "429" in str(e):
            return {"search_query": "", "error": "quota"}
    return {"search_query": "Inception"}

def generate_chat_response(model, user_message: str, recommended_movies: list) -> str:
    titles = [m["title"] for m in recommended_movies]
    return f"🎬 Based on your request, here are 5 great picks: {', '.join(titles)}. Enjoy!"