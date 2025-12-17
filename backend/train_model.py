import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib


# Load dataset
df = pd.read_csv('books_regression.csv')


# Encode genre (categorical → numeric)
le = LabelEncoder()
df['genre_encoded'] = le.fit_transform(df['genre'])


# Features (X) and Target (y)
X = df[['genre_encoded', 'pages', 'difficulty']]
y = df['user_rating']


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42
)


# Train regression model
model = LinearRegression()
model.fit(X_train, y_train)


# Evaluation
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print("Model trained successfully")
print("Mean Squared Error:", mse)


# Save model and encoder
joblib.dump(model, 'book_rating_model.pkl')
joblib.dump(le, 'genre_encoder.pkl')