import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
df = pd.read_csv("books_regression.csv")

# Encode genre
encoder = LabelEncoder()
df["genre_encoded"] = encoder.fit_transform(df["genre"])

# Features and target
X = df[["genre_encoded", "pages", "difficulty"]]
y = df["user_rating"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Training completed")
print("Mean Squared Error:", mse)
print("R2 Score:", r2)

# Save model and encoder
joblib.dump(model, "book_rating_model.pkl")
joblib.dump(encoder, "genre_encoder.pkl")

# =========================
#  GRAPH 1: Actual vs Predicted
# =========================
plt.figure()
plt.scatter(y_test, y_pred)
plt.xlabel("Actual Ratings")
plt.ylabel("Predicted Ratings")
plt.title("Actual vs Predicted Book Ratings")
plt.show()

# =========================
#  GRAPH 2: Prediction Error
# =========================
errors = y_test - y_pred

plt.figure()
plt.scatter(y_pred, errors)
plt.axhline(y=0)
plt.xlabel("Predicted Ratings")
plt.ylabel("Error")
plt.title("Prediction Error Plot")
plt.show()
