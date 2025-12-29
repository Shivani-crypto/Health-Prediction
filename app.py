import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import joblib


# Flask app setup
app = Flask(__name__)

# Load ML model and scaler
model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Login page
@app.route('/login')
def login():
    return render_template('signin.html')

# Home after login
@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            # Get all 13 inputs
            features = [
                float(request.form['age']),
                float(request.form['sex']),
                float(request.form['cp']),
                float(request.form['trestbps']),
                float(request.form['chol']),
                float(request.form['fbs']),
                float(request.form['restecg']),
                float(request.form['thalach']),
                float(request.form['exang']),
                float(request.form['oldpeak']),
                float(request.form['slope']),
                float(request.form['ca']),
                float(request.form['thal'])
            ]

            # Prepare and scale
            data = np.array([features])
            data = scaler.transform(data)

            # Predict
            prediction = model.predict(data)[0]
            result = "High Risk" if prediction == 0 else "Low Risk"


        except Exception as e:
            result = f"Error: {str(e)}"

        return render_template("result.html", result=result)

    return render_template("home.html")


# Sign-in page
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        user = request.form.get('user', '')
        password = request.form.get('password', '')

        # Temporary admin login check
        if user == 'admin' and password == 'admin':
            return render_template("home.html")
        else:
            return render_template("signin.html", message="Invalid username or password.")


if __name__ == '__main__':
    app.run()
