from flask import Flask, render_template, request, redirect, url_for
import joblib

app = Flask(__name__)

# Load trained model and vectorizer
model = joblib.load("models/url_model.pkl")
vectorizer = joblib.load("models/url_vectorizer.pkl")


@app.route("/", methods=["GET", "POST"])
def home():

    result = request.args.get("result")
    url = request.args.get("url", "")

    if request.method == "POST":
        url = request.form["url"]

        # Convert URL into numerical features
        url_features = vectorizer.transform([url])

        # Predict URL
        prediction = model.predict(url_features)[0]

        if prediction == 1:
            result = "LEGITIMATE URL"
        else:
            result = "PHISHING URL"

        return redirect(url_for("home", result=result, url=url))
    return render_template("index.html", result=result, url=url)

if __name__ == "__main__":
    app.run(debug=True)