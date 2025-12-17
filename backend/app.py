from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
from chatbot import chatbot_response

app = Flask(__name__)
CORS(app)

# Load trained model and encoder
model = joblib.load("book_rating_model.pkl")
encoder = joblib.load("genre_encoder.pkl")

# Load dataset
df = pd.read_csv("books_regression.csv")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json

    genre = data["genre"]
    pages = int(data["pages"])
    difficulty = int(data["difficulty"])

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

    return jsonify({
        "predicted_rating": round(float(predicted_rating), 2),
        "recommended_books": recommendations
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data["message"]

    reply = chatbot_response(user_message)

    return jsonify({
        "reply": reply
    })


if __name__ == "__main__":
    app.run(debug=True)
