from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
