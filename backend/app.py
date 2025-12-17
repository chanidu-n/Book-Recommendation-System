from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

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

    # Encode genre
    genre_encoded = encoder.transform([genre])[0]

    # Predict rating
    predicted_rating = model.predict(
        [[genre_encoded, pages, difficulty]]
    )[0]

    # Recommend top books from same genre
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


if __name__ == "__main__":
    app.run(debug=True)
