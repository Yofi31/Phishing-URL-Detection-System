from flask import Flask, render_template, request, redirect, url_for
import joblib
from urllib.parse import urlparse

app = Flask(__name__)

# Load trained model and vectorizer
model = joblib.load("models/url_model.pkl")
vectorizer = joblib.load("models/url_vectorizer.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    result = request.args.get("result")
    url = request.args.get("url", "")
    confidence = request.args.get("confidence")

    if request.method == "POST":
        url = request.form["url"]
        parsed_url = urlparse(url)

        if not parsed_url.scheme or not parsed_url.netloc:
            return redirect(url_for("home", result="INVALID URL", url=url))
        
        if "." not in parsed_url.netloc:
            return redirect(url_for("home", result="INVALID URL", url=url))

        # Convert URL into numerical features
        url_features = vectorizer.transform([url])

        # Predict URL
        prediction = model.predict(url_features)[0]
        probabilities = model.predict_proba(url_features)[0]
        confidence = round(probabilities[prediction] * 100, 2)

        if prediction == 1:
            result = "LEGITIMATE URL"
        else:
            result = "PHISHING URL"

        return redirect(url_for("home", result=result, url=url, confidence=confidence))
    return render_template("index.html", result=result, url=url, confidence=confidence)

if __name__ == "__main__":
    app.run(debug=True)