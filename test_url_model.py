import joblib

# Load trained model and vectorizer
model = joblib.load("models/url_model.pkl")
vectorizer = joblib.load("models/url_vectorizer.pkl")

print("Phishing URL Detection System")
print("Type 'exit' to stop the program.")

while True:
    url = input("\nEnter a URL: ")

    if url.lower() == "exit":
        print("Program stopped.")
        break

    # Convert URL into numerical features
    url_features = vectorizer.transform([url])

    # Predict URL
    prediction = model.predict(url_features)[0]

    if prediction == 1:
        print("Result: LEGITIMATE URL")
    else:
        print("Result: PHISHING URL")