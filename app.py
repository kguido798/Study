from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ CREATE APP FIRST
app = Flask(__name__)

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = "udemy-course-scraper-api.p.rapidapi.com"


# ✅ THEN DEFINE ROUTES
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    price = request.args.get('price')

    if not query:
        return jsonify({"error": "Please enter a search term"}), 400

    url = f"https://classroom.googleapis.com/v1/courses"

    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    params = {"query": query}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        courses = []

        for item in data.get("courses", [])[:20]:
            course = {
                "title": item.get("title"),
                "provider": "Udemy",
                "rating": item.get("rating"),
                "price": item.get("price"),
                "duration": item.get("duration", "N/A"),
                "url": item.get("url")
            }

            if price == "free" and course["price"] != "Free":
                continue
            if price == "paid" and course["price"] == "Free":
                continue

            courses.append(course)

        return jsonify(courses)

    except Exception:
        return jsonify({"error": "API request failed"}), 500


# ✅ RUN LAST
if __name__ == '__main__':
    app.run(debug=True)
