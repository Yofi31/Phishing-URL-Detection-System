import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
data = pd.read_csv("dataset/PhiUSIIL_Phishing_URL_Dataset.csv")

print("Dataset loaded successfully.")
print("Dataset shape:", data.shape)

# URL text is the input
X = data["URL"].astype(str)

# Label is the output
y = data["label"]

print("\nLabel distribution:")
print(y.value_counts())

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

# Convert URLs into numerical features
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(3, 5),
    max_features=50000
)

print("\nConverting URLs into numerical features...")

X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

print("URL conversion completed.")

# Create model
model = LogisticRegression(
    max_iter=1000
)

print("\nTraining URL model...")

# Train model
model.fit(X_train_vectorized, y_train)

print("Model training completed.")

# Test model
y_pred = model.predict(X_test_vectorized)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Create models folder
os.makedirs("models", exist_ok=True)

# Save model
joblib.dump(model, "models/url_model.pkl")

# Save vectorizer
joblib.dump(vectorizer, "models/url_vectorizer.pkl")

print("\nURL model saved successfully.")