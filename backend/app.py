from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from chatbot import chatbot_response, get_genre_info

app = Flask(__name__)
CORS(app)

# Load trained model and encoder
model = joblib.load("book_rating_model.pkl")
encoder = joblib.load("genre_encoder.pkl")

# Load dataset
df = pd.read_csv("books_regression.csv")


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        genre = data.get("genre")
        pages = data.get("pages")
        difficulty = data.get("difficulty")

        if not all([genre, pages, difficulty]):
            return jsonify({"error": "Missing required fields: genre, pages, difficulty"}), 400

        pages = int(pages)
        difficulty = int(difficulty)

        genre_encoded = encoder.transform([genre])[0]

        predicted_rating = model.predict(
            [[genre_encoded, pages, difficulty]]
        )[0]

        recommendations = (
            df[df["genre"] == genre]
            .sort_values(by="user_rating", ascending=False)
            .head(3)["title"]
            .tolist()
        )

        if not recommendations:
            recommendations = ["No books found for this genre. Try another!"]

        return jsonify({
            "predicted_rating": round(float(predicted_rating), 2),
            "recommended_books": recommendations
        })
    
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        
        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data["message"].strip()
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        reply = chatbot_response(user_message)

        return jsonify({
            "reply": reply
        })
    
    except Exception as e:
        return jsonify({"error": f"Chat error: {str(e)}"}), 500


@app.route("/genre-info/<genre>", methods=["GET"])
def genre_info(genre):
    """New endpoint to get genre information"""
    try:
        info = get_genre_info(genre)
        
        # Get top books in this genre
        if genre in df['genre'].values:
            top_books = df[df['genre'] == genre].nlargest(5, 'user_rating')[['title', 'user_rating']].to_dict('records')
        else:
            top_books = []
        
        return jsonify({
            "genre": genre,
            "info": info,
            "top_books": top_books
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
